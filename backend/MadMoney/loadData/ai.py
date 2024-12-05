import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import ollama
from MadMoney.essentials import env_to_var


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Function {func.__name__} took {end_time - start_time:.2f} seconds to complete"
        )
        return result

    return wrapper


# @timing_decorator
def get_chat_completion(message):
    max_tokens = 8000
    conversation_history = []

    messages = [message[i : i + max_tokens] for i in range(0, len(message), max_tokens)]
    messages = messages[:1]  # fix later...

    chat_completion = None
    for msg in messages:

        conversation_history.append({"role": "user", "content": msg})

        chat_completion = ollama.chat(
            messages=conversation_history,
            model="qwen2.5",
        )

        conversation_history.append(
            {"role": "assistant", "content": chat_completion["message"]["content"]}
        )

    return conversation_history[-1]["content"] if chat_completion else None


if __name__ == "__main__":
    response = get_chat_completion("hello " * 5000)
    print(response)
