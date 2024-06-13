import unittest
from io import StringIO
from unittest.mock import patch, mock_open

from interpreter import *


class TestBefungeInterpreter(unittest.TestCase):
    def setUp(self):
        self.pointer = Pointer([])

    def test_peek(self):
        self.pointer.stack.push(4)
        self.assertEqual(self.pointer.stack.peek(), 4)
        self.pointer.stack.push(5)
        self.assertEqual(self.pointer.stack.peek(), 5)
        self.pointer.stack.pop()
        self.assertEqual(self.pointer.stack.peek(), 4)

    def test_is_empty(self):
        self.assertTrue(self.pointer.stack.is_empty())
        self.pointer.stack.push(6)
        self.assertFalse(self.pointer.stack.is_empty())
        self.pointer.stack.pop()
        self.assertTrue(self.pointer.stack.is_empty())

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

    def test_string_mode_command(self):
        self.pointer.is_string = False
        StringModeCommand().execute(self.pointer)
        self.assertTrue(self.pointer.is_string)

    def test_random_command(self):
        RandomCommand().execute(self.pointer)
        self.assertIn(self.pointer.vector.get_vector(),
                      [(0, 1), (0, -1), (1, 0), (-1, 0)])

    def test_stop_command(self):
        StopCommand().execute(self.pointer)
        self.assertTrue(self.pointer.stop)

    @patch('builtins.input', side_effect=['9'])
    def test_input_number_command(self, _):
        InputNumberCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 9)

    @patch('builtins.input', side_effect=['a'])
    def test_input_char_command(self, _):
        InputCharCommand().execute(self.pointer)
        self.assertEqual(self.pointer.stack.pop(), 97)

    def test_get_code_from_file(self):
        with open('test_code.bf', 'w') as f:
            f.write('123@')

        with patch('sys.argv', ['interpreter.py', 'test_code.bf']), \
                patch('sys.stdin', StringIO('')):
            code = get_code()
        self.assertEqual(code, ['123@'])

    @patch('sys.stdin' ,create=True)
    def test_get_code_from_input(self, mock_stdin):
        mock_stdin.readline.side_effect = ['>987v>.v\n', 'v456<  :\n',
                                           '2v   ,&<\n', '1>:&:v\n',
                                           ' ^   _@ \n', 'Q\n']
        test_args = ['program', 'mycode']
        with patch.object(sys, 'argv', test_args):
            result = get_code()
            expected = ['>987v>.v', 'v456<  :', '2v   ,&<',
                        '1>:&:v', '^   _@']
            self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_code_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        test_args = ['program', 'nonexistent.bf']
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                get_code()
            self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
