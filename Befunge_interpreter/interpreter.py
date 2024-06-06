from interpreter_config import *


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python interpreter.py <file.bf>')
        sys.exit(0)

    bf_file = sys.argv[1]
    try:
        if sys.argv[1] == 'mycode':
            code = []
            stop_char = 'Q'
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

    interpreter = Pointer(code)
    interpreter.execute()
    print(interpreter.output)


if __name__ == '__main__':
    main()
