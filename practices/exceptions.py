#!/usr/bin/env python

import sys


def f0():
    5 / 0


def f1():
    5 / 0


def f2():
    5 / 0


def f3():
    print("Sdsd")


def f4():
    a = 3216
    result = 2.1 / (17.2 ** a) - 12.3 / (4.4 + 2.0 * a) + 14.4 / (9.2 * 4.0 + 2.1) + 1.1 * (2.1 / 3.6 * a)
    print(result)


def f5():
    0 ** (-1)


def f6():
    print(12222)


def f7():
    class Attribute():
        def __init__(self):
            self.leng = 20

            self.bred = 10
            self.area = self.leng * self.bred

    A = Attribute()
    print(A.ar)


def f8():
    raise EnvironmentError


def f9():
    from os import subprocess


def f10():
    raise LookupError


def f11():
    raise IndexError


def f12():
    raise KeyError


def f13():
    raise NameError


def f14():
    raise SyntaxError


def f15():
    raise ValueError


def f16():
    raise UnicodeError


def check_exception(f, exception):
    try:
        f()
    except exception as e:
        print(e)
    else:
        print("Bad luck, no exception caught: %s" % exception)


check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")
