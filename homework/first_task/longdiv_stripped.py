#!/usr/bin/env python3


def long_division(dividend, divider):
    pointer_dividend = 0
    tab_count = 0
    str_dividend = str(dividend)
    output_string = f"{dividend}|{divider}\n"
    flag = True

    # Определяем число, которое делим первым
    if len(str_dividend) != 1:
        new_dividend = dividend  # Initialize with a default value
        for pointer_dividend in range(1, len(str_dividend) - 1):
            flag = False
            if (int(str_dividend[:pointer_dividend]) // divider) != 0:
                new_dividend = int(str_dividend[:pointer_dividend])
                break
            else:
                new_dividend = dividend
        if flag is True:
            new_dividend = dividend
    else:
        new_dividend = dividend

    str_new_dividend = str(new_dividend)
    tab_to_end = " " * (len(str_dividend) - len(str_new_dividend))
    subtraction_number = (new_dividend // divider) * divider

    if len(str_dividend) != 1:
        pointer_dividend -= 1

    # Записываем вторую строку в зависимости от делимого
    if subtraction_number != 0:
        output_string += (f"{subtraction_number}{tab_to_end}|"
                          f"{dividend // divider}\n")
    else:
        output_string += f"{dividend}{tab_to_end}|{dividend // divider}\n"

    # Цикл, который выполняет деление
    while subtraction_number != 0:
        str_old_dividend = str(new_dividend)
        new_dividend = new_dividend - subtraction_number
        tab_count += len(str_old_dividend) - len(str(new_dividend))

        # Добавляем табы, в зависимости от длины числа
        if len(str_old_dividend) == 1 and len(str(new_dividend)) == 1:
            if dividend != 1:  # Оно делало таб для случая с 1 (
                tab_count += 1

        # Тут мы обновляем new_dividend, пока не кончится dividend
        if new_dividend // divider == 0:
            while pointer_dividend != len(str_dividend) - 1:
                pointer_dividend += 1
                new_dividend = int(str(new_dividend)
                                   + str_dividend[pointer_dividend])
                if new_dividend // divider != 0:
                    subtraction_number = (new_dividend // divider) * divider
                    break
            if dividend - subtraction_number == 0:
                subtraction_number = 0
            elif pointer_dividend == len(str_dividend) - 1:
                if (new_dividend != int(str_dividend[pointer_dividend]) or
                        new_dividend == 0):
                    subtraction_number = (new_dividend // divider) * divider
                else:
                    subtraction_number = (new_dividend // divider) * divider
                    tab_count = pointer_dividend
        else:
            subtraction_number = (new_dividend // divider) * divider

        # Тут я накидал какой-то костыль
        if subtraction_number == 0 and dividend % divider != 0:
            output_string += f"{' ' * tab_count}{new_dividend}\n"
        elif dividend == divider:
            output_string += f"{' ' * tab_count}{subtraction_number}\n"
        elif subtraction_number == 0 and dividend % divider == 0:
            if divider == 1:
                tab_count -= 1
            output_string += f"{' ' * tab_count}{subtraction_number}\n"
        else:
            output_string += (f"{' ' * tab_count}{new_dividend}\n"
                              f"{' ' * tab_count}{subtraction_number}\n")

    if output_string[len(output_string) - 1] == "\n":
        output_string = output_string[:-1]

    return output_string


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()
