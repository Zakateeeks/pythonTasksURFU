import unittest
from unittest.mock import patch

from Befunge_interpreter.interpreter_config import *


class TestBefungeInterpreter(unittest.TestCase):
    def setUp(self):
        self.pointer = Pointer([])

    def test_push_and_pop(self):
        self.pointer.stack.push(5)
        self.pointer.stack.push(3)
        self.assertEqual(self.pointer.stack.pop(), 3)
        self.assertEqual(self.pointer.stack.pop(), 5)

    def test_duplicate(self):
        self.pointer.stack.push(7)
        self.pointer.stack.duplicate()
        self.assertEqual(self.pointer.stack.pop(), 7)
        self.assertEqual(self.pointer.stack.pop(), 7)

    def test_swap(self):
        self.pointer.stack.push(1)
        self.pointer.stack.push(2)
        self.pointer.stack.swap()
        self.assertEqual(self.pointer.stack.pop(), 1)
        self.assertEqual(self.pointer.stack.pop(), 2)

    def test_add_command(self):
        self.pointer.stack.push(2)
        self.pointer.stack.push(3)
        AddCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 5)

    def test_subtract_command(self):
        self.pointer.stack.push(5)
        self.pointer.stack.push(3)
        SubCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 2)

    def test_multiply_command(self):
        self.pointer.stack.push(4)
        self.pointer.stack.push(3)
        MultiplyCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 12)

    def test_divide_command(self):
        self.pointer.stack.push(8)
        self.pointer.stack.push(2)
        DivideCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 4)

    def test_module_command(self):
        self.pointer.stack.push(10)
        self.pointer.stack.push(3)
        ModuleCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 1)

    def test_not_command(self):
        self.pointer.stack.push(0)
        NotCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 1)
        self.pointer.stack.push(1)
        NotCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 0)

    def test_comparison_command(self):
        self.pointer.stack.push(2)
        self.pointer.stack.push(3)
        ComparisonCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 0)
        self.pointer.stack.push(3)
        self.pointer.stack.push(2)
        ComparisonCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 1)

    def test_direction_commands(self):
        RightCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (0, 1))
        LeftCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (0, -1))
        UpCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (-1, 0))
        DownCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (1, 0))

    def test_conditional_commands(self):
        self.pointer.stack.push(0)
        ConditionalRightCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (0, 1))
        self.pointer.stack.push(1)
        ConditionalRightCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (0, -1))
        self.pointer.stack.push(0)
        ConditionalUpCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (1, 0))
        self.pointer.stack.push(1)
        ConditionalUpCommand().execute(self.pointer)
        self.assertEqual(self.pointer.vector.get_vector(), (1, 0))

    def test_output_commands(self):
        self.pointer.stack.push(65)
        OutputCharCommand().execute(self.pointer)
        self.assertEqual(self.pointer.output, 'A')
        self.pointer.stack.push(123)
        OutputIntCommand().execute(self.pointer)
        self.assertEqual(self.pointer.output, 'A123')

    @patch('builtins.input', side_effect=['9'])
    def test_input_number_command(self, mock_input):
        InputNumberCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 9)

    @patch('builtins.input', side_effect=['a'])
    def test_input_char_command(self, mock_input):
        InputCharCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 97)


if __name__ == '__main__':
    unittest.main()
