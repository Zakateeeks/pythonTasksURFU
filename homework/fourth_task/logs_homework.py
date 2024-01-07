import sys


def get_max_value(filename, index):
    max_value = [0, 0]

    with open(filename, 'r', encoding='cp1251', errors='ignore') as file:
        data_dict = dict()

        for data_array in (line.split(',') for line in file):
            data_value = data_array[index]
            data_dict[data_value] = data_dict.get(data_value, 0) + 1

        for data_value, count in data_dict.items():
            if count > max_value[0]:
                max_value[1] = data_value
                max_value[0] = count

    return max_value


def user_active(filename):
    max_value = get_max_value(filename, 0)
    print("Самый активный клиент:", max_value)


def service_popular(filename):
    max_value = get_max_value(filename, 13)
    print("Самый популярный сервис:", max_value)


if __name__ == "__main__":
    x = sys.argv[len(sys.argv) - 1]
    if x == "user":
        user_active('W3SVC6.log')
    elif x == "service":
        service_popular('W3SVC6.log')
    else:
        x = sys.argv[0]
        user_active('W3SVC6.log')
        service_popular('W3SVC6.log')
