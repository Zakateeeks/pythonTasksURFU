import argparse

from interpreter_config import *


def get_code() -> list[str]:
    """
    :return: code
    """
    parser = argparse.ArgumentParser(description='Befunge interpreter')
    parser.add_argument('file', help='The .bf file to execute'
                                     'or "mycode" to input code')
    args = parser.parse_args()

    bf_file = args.file

    try:
        if bf_file == 'mycode':
            code = []
            stop_char = 'Q'
            print("Enter your Befunge code line by line."
                  " Enter 'Q' to finish.")
            while True:
                line = sys.stdin.readline().strip()
                if line == stop_char:
                    break
                code.append(line)
        else:
            with open(bf_file) as file:
                code = file.readlines()
    except FileNotFoundError:
        print(f'File {bf_file} not found')
        sys.exit(0)

    return code


def main() -> None:
    code = get_code()

    interpreter = Pointer(code)
    interpreter.execute()
    print(interpreter.output)


if __name__ == '__main__':
    main()
