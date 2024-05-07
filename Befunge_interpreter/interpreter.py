import sys

from interpreter_config import *


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python interpreter.py <file.bf>')
        sys.exit(0)

    bf_file = sys.argv[1]
    try:
        with open(bf_file) as file:
            code = file.readlines()
    except FileNotFoundError:
        print(f"File {bf_file} not found")
        sys.exit(0)

    interpreter = Pointer(code)
    interpreter.action()
    print(interpreter.output)


if __name__ == '__main__':
    main()
