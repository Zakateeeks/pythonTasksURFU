import random
import sys
from abc import ABC, abstractmethod
from typing import Tuple, List, NoReturn, Dict


class Stack:
    """
    The class is designed to work with the stack.

    push() - Adds an item to the stack
    pop() - Returns an element at the top of the stack and deletes it
    duplicate() - Copies a stack top and adds it to the stack
    swap() - Swaps the top and sub-top of the stack.
    peek() - Returns an item at the top of the stack without deleting it.
    is_empty() - Checks if the stack is empty
    """

    def __init__(self) -> NoReturn:
        self.stack: List[int] = []

    def push(self, value: int) -> NoReturn:
        """
        Adds an item to the stack.

        Args
        ----------
        value : int
            The value to add to the stack.
        """
        self.stack.append(value)

    def pop(self) -> int:
        """
         Returns and removes an element at the top of the stack.

         Returns
         ----------
         int: The top element of the stack or 0 if the stack is empty.
         """
        return self.stack.pop() if self.stack else 0

    def duplicate(self) -> NoReturn:
        """
        Copies the top item of the stack and adds it to the stack.
        """
        if self.stack:
            self.push(self.stack[-1])

    def swap(self) -> NoReturn:
        """
        Swaps the top and sub-top items of the stack.
        """
        if len(self.stack) > 1:
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def peek(self) -> int:
        """
        Returns an item at the top of the stack without removing it.

        Returns
        ----------
        int: The top element of the stack or 0 if the stack is empty.
        """
        return self.stack[-1] if self.stack else 0

    def is_empty(self) -> bool:
        """
        Checks if the stack is empty.

        Returns
        ----------
        bool: True if the stack is empty, False otherwise.
        """
        return len(self.stack) == 0


class Vector:
    """
    The class is designed to indicate the direction of travel

    set_vector() - Sets the direction of motion
    get_vector() - Returns the direction of motion
    """

    def __init__(self):
        self.vector: Tuple[int, int] = (0, 1)

    def set_vector(self, new_vector: Tuple[int, int]) -> NoReturn:
        """
        Sets the direction of motion.

        Args
        ----------
        new_vector : Tuple[int, int]
            The new direction vector.
        """
        self.vector = new_vector

    def get_vector(self) -> Tuple[int, int]:
        """
        Returns the direction of motion.

        Returns
        ----------
        Tuple[int, int]: The current direction vector.
        """
        return self.vector


class Position:
    """
    The class is created to specify the position

    move() - Moves the position based on the direction of movement
    get_position() - Returns the current position
    """

    def __init__(self) -> NoReturn:
        self.position: Tuple[int, int] = (0, 0)

    def move(self, vector: Tuple[int, int]) -> NoReturn:
        """
        Moves the position based on the direction of movement.

        Args
        ----------
        vector : Tuple[int, int]
            The direction vector for movement.
        """
        self.position = (self.position[0] + vector[0],
                         self.position[1] + vector[1])

    def get_position(self) -> Tuple[int, int]:
        """
        Returns the current position.

        Returns
        ----------
        Tuple[int, int]: The current position coordinates.
        """
        return self.position


class Code:
    """
    The class is created to work with Befunge language code

    get_symbol() - Gets a symbol from Befunge code
    update_code() - Updates the symbol by specified coordinates
    get_value() - Returns the symbol at the given coordinates
    """

    def __init__(self, code: List[str]):
        self.code = code

    def get_symbol(self, position: Tuple[int, int]) -> str:
        """
        Gets a symbol from Befunge code.

        Args
        ----------
        position : Tuple[int, int]
            The coordinates of the symbol.

        Returns
        ----------
        str: The symbol at the specified coordinates.
        """
        try:
            return self.code[position[0]][position[1]]
        except IndexError:
            print('Your code is incorrect')
            sys.exit(0)

    def update_code(self, y: int, x: int, v: int) -> NoReturn:
        """
        Updates the symbol at specified coordinates.

        Args
        ----------
        y : int
            The y-coordinate.
        x : int
            The x-coordinate.
        v : int
            The new value to set.
        """
        self.code[y] = self.code[y][:x] + chr(v) + self.code[y][x + 1]

    def get_value(self, y: int, x: int) -> int:
        """
        Returns the value of the symbol at the given coordinates.

        Args
        ----------
        y : int
            The y-coordinate.
        x : int
            The x-coordinate.

        Returns
        ----------
        int: The ASCII value of the symbol at the specified coordinates.
        """
        return ord(self.code[y][x])


class Command(ABC):
    """
    Abstract class, with its help Befunge language commands are implemented
    """

    @abstractmethod
    def execute(self, pointer: 'Pointer') -> NoReturn:
        pass


class AddCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.push(pointer.stack.pop() + pointer.stack.pop())


class SubCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.push(pointer.stack.pop() - pointer.stack.pop())


class MultiplyCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.push(pointer.stack.pop() * pointer.stack.pop())


class DivideCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.push(pointer.stack.pop() // pointer.stack.pop())


class ModuleCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.push(pointer.stack.pop() % pointer.stack.pop())


class NotCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        self.stack.push(int(not pointer.stack.pop))


class ComparisonCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        self.stack.push(int(pointer.stack.pop() <
                            pointer.stack.pop()))


class RightCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector((0, 1))


class LeftCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector((0, -1))


class UpCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector((-1, 0))


class DownCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector((1, 0))


class RandomCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector(random.choice([(0, 1), (0, -1),
                                                 (1, 0), (-1, 0)]))


class ConditionalRightCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector((0, 1) if pointer.stack.pop() == 0
                                  else (0, -1))


class ConditionalUpCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.vector.set_vector((-1, 0) if pointer.stack.pop == 0
                                  else (1, 0))


class StringModeCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.is_string = not pointer.is_string


class DuplicateCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.duplicate()


class SwapCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.swap()


class PopCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.pop()


class OutputIntCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.output += str(pointer.stack.pop())


class OutputCharCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        peak = pointer.stack.pop()
        pointer.output += chr(peak)


class SkipCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.steps()


class PutCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        y, x, v = (pointer.stack.pop(), pointer.stack.pop(),
                   pointer.stack.pop())
        pointer.code.update_code(y, x, v)


class GetCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        y, x = pointer.stack.pop(), pointer.stack.pop()
        pointer.stack.push(pointer.code.get_value(y, x))


class InputNumberCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        value = int(input('Enter a number: '))
        pointer.stack.push(value)


class InputCharCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        value = input("Enter a symbol: ")
        pointer.stack.push(ord(value[0]))


class StopCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stop = True


class QuiteCommand(Command):
    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        value = pointer.stack.pop()
        sys.exit(value)


class HexCommand(Command):
    def __init__(self, value: int) -> NoReturn:
        self.value = value

    def execute(self, pointer: 'Pointer') -> NoReturn:
        """


        Args
        ----------
        pointer : Pointer
            The pointer object.
        """
        pointer.stack.push(self.value)


class Pointer:
    COMMANDS: Dict[str, Command] = {
        '+': AddCommand(),
        '-': SubCommand(),
        '*': MultiplyCommand(),
        '/': DivideCommand(),
        '%': ModuleCommand(),
        '!': NotCommand(),
        '`': ComparisonCommand(),
        '>': RightCommand(),
        '<': LeftCommand(),
        '^': UpCommand(),
        'v': DownCommand(),
        '?': RandomCommand(),
        '_': ConditionalRightCommand(),
        '|': ConditionalUpCommand(),
        '"': StringModeCommand(),
        ':': DuplicateCommand(),
        '\\': SwapCommand(),
        '$': PopCommand(),
        '.': OutputIntCommand(),
        ',': OutputCharCommand(),
        '#': SkipCommand(),
        'p': PutCommand(),
        'g': GetCommand(),
        '&': InputNumberCommand(),
        '~': InputCharCommand(),
        'q': QuiteCommand(),
        'a': HexCommand(10),
        'b': HexCommand(11),
        'c': HexCommand(12),
        'd': HexCommand(13),
        'e': HexCommand(14),
        'f': HexCommand(15),
        '@': StopCommand()
    }

    def __init__(self, code: List[str]) -> NoReturn:

        self.code = Code(code)
        self.stack = Stack()
        self.vector = Vector()
        self.position = Position()
        self.is_string = False
        self.output = ''
        self.stop = False

    def steps(self) -> NoReturn:
        """
        Move the pointer one step in the direction of the vector.
        """
        self.position.move(self.vector.get_vector())

    def execute(self) -> NoReturn:
        """
        Here we work with the character from the bf code,
        which is currently pointed to by the pointer
        """
        while not self.stop:
            symbol = self.code.get_symbol(self.position.get_position())
            if self.is_string:
                if symbol == '"':
                    self.is_string = False
                else:
                    self.stack.push(ord(symbol))
            else:
                command = self.COMMANDS.get(symbol)
                if command:
                    command.execute(self)
                elif symbol.isdigit():
                    self.stack.push(int(symbol))
            self.steps()
