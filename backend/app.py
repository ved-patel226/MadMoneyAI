import os

import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from flask_cors import CORS, cross_origin
from MadMoney import *

from celery import Celery
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": "http://localhost:5173",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

app.config["JWT_SECRET_KEY"] = "secretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

jwt = JWTManager(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

full_path = os.path.join(os.getcwd(), "..", "frontend", ".env")
load_dotenv(dotenv_path=full_path)


try:
    GOOGLE_CLIENT_ID = os.environ["VITE_GOOGLE_CLIENT_ID"]
    GOOGLE_SECRET_KEY = os.environ["GOOGLE_SECRET_KEY"]
except:
    load_dotenv(dotenv_path="frontend/.env")
    GOOGLE_CLIENT_ID = os.environ["VITE_GOOGLE_CLIENT_ID"]
    GOOGLE_SECRET_KEY = os.environ["GOOGLE_SECRET_KEY"]


@app.route("/", methods=["GET"])
def hello_world():
    return "hello world"


@app.route("/google_login", methods=["POST"])
def login():
    auth_code = request.get_json()["code"]

    data = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_SECRET_KEY,
        "redirect_uri": "postmessage",
        "grant_type": "authorization_code",
    }

    response = requests.post("https://oauth2.googleapis.com/token", data=data).json()
    headers = {"Authorization": f'Bearer {response["access_token"]}'}
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", headers=headers
    ).json()

    jwt_token = create_access_token(identity=user_info["email"])
    response = jsonify(user=user_info)
    response.set_cookie("access_token_cookie", value=jwt_token, secure=True)

    return response, 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    jwt_token = request.cookies.get("access_token_cookie")
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/check/created/today")
def check_created_today():
    return jsonify(API.check_created_today()), 200


@celery.task(bind=True)
def long_running_task(self):
    total_steps = 5
    current_step = 0

    functions = {
        0: lambda: download_audio_as_wav(get_latest_video()),
        1: trim_audio(short=True),
        2: convert_to_json,
        3: prompt_result_mongo,
        4: check_json_ticker,
    }

    try:
        for step in range(total_steps):

            function = functions.get(step)
            if function:
                function()
                current_step = step + 1

            self.update_state(
                state="PROGRESS", meta={"current": current_step, "total": total_steps}
            )

        return {
            "status": "Task completed successfully!",
            "current": current_step,
            "total": total_steps,
            "data": API.get_recent(),
        }

    except Exception as e:
        raise self.retry(exc=e)


@app.route("/create/today", methods=["GET"])
@jwt_required(optional=True)
def create_today():
    if API.check_created_today():
        return jsonify({"error": "Already created today"}), 200

    task = long_running_task.apply_async()
    return jsonify({"task_id": task.id}), 202


@app.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = long_running_task.AsyncResult(task_id)

    if task.state == "PENDING":

        response = {"state": task.state, "progress": 0}
    elif task.state == "PROGRESS":

        current = task.info.get("current", 0)
        total = task.info.get("total", 1)
        progress = (current * 100) // total
        response = {"state": task.state, "progress": progress}
    elif task.state == "SUCCESS":

        response = {"state": task.state, "progress": 100, "result": task.result}
    else:

        response = {"state": task.state, "progress": 0, "error": str(task.info)}

    return jsonify(response)


@app.route("/is_authenticated", methods=["GET"])
@jwt_required(optional=True)
@cross_origin(origins=["http://localhost:5173"])
def is_authenticated():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(authenticated=True, user=current_user), 200
    else:
        return jsonify(authenticated=False), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
