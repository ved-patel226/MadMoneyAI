import os
from dotenv import load_dotenv


def env_to_var(key: str) -> str:
    if "frontend" in os.getcwd():
        full_path = os.path.join(os.getcwd(), ".env")
    else:
        partial_path = os.getcwd().split("/")[:-1]
        partial_path.append("frontend")
        partial_path = "/".join(partial_path)

        full_path = os.path.join(partial_path, ".env")
        # print(full_path)

    load_dotenv(dotenv_path=full_path)
    # print(os.getenv(key))
    assert os.getenv(key) is not None, f"{key} is not in .env file"

    return os.getenv(key)


if __name__ == "__main__":
    env_to_var("GROQ_KEY")
