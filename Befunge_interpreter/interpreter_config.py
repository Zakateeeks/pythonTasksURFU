class Pointer:
    """
        This class describes the operation of the interpreter

        Attributes:
        code (list): The two-dimensional array with bf code
        stack (list): The stack used for operations.
        vector (tuple): The current movement vector.
        position (tuple): The current position of the pointer.
        is_string (bool): Flag indicating if the pointer is
        currently parsing a string.
        output (str): Program result
    """

    def __init__(self, code: list):
        """
        Initialize Pointer with code, stack, vector, position,
         is_string, and output.


        :param code: The two-dimensional array with bf code
        """
        self.code = code
        self.stack = []
        self.vector = (0, 1)
        self.position = (0, 0)
        self.is_string = False
        self.output = ''

    def steps(self):
        """
        Move the pointer one step in the direction of the vector.
        """
        self.position = ((self.position[0] + self.vector[0]),
                         (self.position[1] + self.vector[1]))

    def action(self):
        """
        Here we work with the character from the bf code,
        which is currently pointed to by the pointer
        """
        while True:
            symbol = self.code[self.position[0]][self.position[1]]
            if self.is_string:
                if symbol == '"':
                    self.is_string = False
                else:
                    self.stack.append(ord(symbol))
            else:
                if symbol.isdigit():
                    self.stack.append(int(symbol))
                elif symbol == '+':
                    self.stack.append(self.stack.pop() + self.stack.pop())
                elif symbol == '-':
                    self.stack.append(self.stack.pop() - self.stack.pop())
                elif symbol == '*':
                    self.stack.append(self.stack.pop() * self.stack.pop())
                elif symbol == '/':
                    self.stack.append(self.stack.pop() // self.stack.pop())
                elif symbol == '%':
                    self.stack.append(self.stack.pop() % self.stack.pop())
                elif symbol == '!':
                    self.stack.append(int(not self.stack.pop()))
                elif symbol == '`':
                    self.stack.append(int(self.stack.pop() <
                                          self.stack.pop()))
                elif symbol == '>':
                    self.vector = (0, 1)
                elif symbol == '<':
                    self.vector = (0, -1)
                elif symbol == '^':
                    self.vector = (-1, 0)
                elif symbol == 'v':
                    self.vector = (1, 0)
                elif symbol == '?':
                    import random
                    arr_vector = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    self.vector = random.choice(arr_vector)
                elif symbol == '_':
                    if len(self.stack) != 0:
                        self.vector = (0, 1) if (
                                self.stack.pop() == 0) else (0, -1)
                    else:
                        self.vector = (0, 1)
                elif symbol == '|':
                    self.vector = (-1, 0) if self.stack.pop() == 0 else (1, 0)
                elif symbol == '"':
                    self.is_string = True
                elif symbol == ':':
                    if len(self.stack) != 0:
                        last = self.stack.pop()
                        self.stack.append(last)
                        self.stack.append(last)
                elif symbol == '\\':
                    peak = self.stack.pop()
                    sub_peak = self.stack.pop()
                    self.stack.append(peak)
                    self.stack.append(sub_peak)
                elif symbol == '$':
                    self.stack.pop()
                elif symbol == '.':
                    peak = self.stack.pop()
                    self.output += str(peak)
                elif symbol == ',':
                    peak = self.stack.pop()
                    self.output += (chr(peak))
                elif symbol == '#':
                    self.steps()
                elif symbol == 'p':
                    y, x, v = (self.stack.pop(), self.stack.pop(),
                               self.stack.pop())
                    self.code[y] = (self.code[y][:x] + chr(v)
                                    + self.code[y][x + 1:])
                elif symbol == 'g':
                    y, x = self.stack.pop(), self.stack.pop()
                    self.stack.append(ord(self.code[y][x]))
                elif symbol == '&':
                    value = int(input('Enter a number: '))
                    self.stack.append(value)
                elif symbol == '~':
                    value = input('Enter a symbol: ')
                    self.stack.append(ord(value[0]))
                elif symbol == '@':
                    break
            self.steps()
