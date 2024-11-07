import os
from dotenv import load_dotenv


def env_to_var(key: str) -> str:
    load_dotenv()
    return os.getenv(key)


if __name__ == "__main__":
    print(env_to_var("GROQ_KEY"))
