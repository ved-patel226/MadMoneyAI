import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from groq import Groq
from MadMoney.essentials import env_to_var


def get_chat_completion(message):
    client = Groq(
        api_key=env_to_var("GROQ_KEY"),
    )

    messages = [message[i : i + 2048] for i in range(0, len(message), 2048)]
    if len(messages) > 3:
        print("LLM MIGHT TAKE A WHILE TO RESPOND")

    chat_completion = None
    for msg in messages:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": msg,
                }
            ],
            model="llama-3.1-70b-versatile",
        )

    return chat_completion.choices[0].message.content if chat_completion else None


if __name__ == "__main__":
    response = get_chat_completion("hello " * 2048)
    print(response)
