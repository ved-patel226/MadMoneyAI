import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from MadMoney.essentials import env_to_var


def test_env_to_var():
    assert len(env_to_var("MONGO_URI")) == 106


def main() -> None:
    test_env_to_var()


if __name__ == "__main__":
    main()
