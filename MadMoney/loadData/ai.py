import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from groq import Groq
from MadMoney.essentials import env_to_var


def get_chat_completion(message):
    client = Groq(
        api_key=env_to_var("GROQ_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    response = get_chat_completion("hello")
    print(response)
