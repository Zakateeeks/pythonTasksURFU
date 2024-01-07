#!/usr/bin/env python3

womens = {'Елена', 'Анна', 'Алина', 'Ксения', 'Лидия', 'Вероника',
          'Ирина', 'Екатерина', 'Кристина', 'Евдокия', 'Наталья',
          'Ольга', 'Валерия', 'Анастасия', 'Алена', 'Софья',
          'Валентина', 'София', 'Дарья', 'Лилия', 'Наташа', 'Яна',
          'Галина', 'Алла', 'Алиса', 'Татьяна', 'Олеся', 'Любовь',
          'Тамара', 'Светлана', 'Оксана', 'Евгения', 'Надежда', 'Юлия',
          'Алёна', 'Александра', 'Марина', 'Елизавета', 'Полина',
          'Эльвера', 'Мария'}


def make_stat(filename):
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """
    with open(filename, 'r', encoding='cp1251') as file:
        page_text = file.read()

    start_index = page_text.find('<body>')
    end_index = page_text.find('</body>')
    filtered_page = page_text[start_index:end_index]

    filtered_page_list = filtered_page.split('<h3>')
    filtered_page_list.pop(0)

    stat_dict = {}

    for page_section in filtered_page_list:
        year = page_section.split('href')[0][:4]
        stat_dict[year] = {'female': [], 'male': []}

        students = page_section.split('href')
        students.pop(0)

        used_names = []

        for student in students:
            name = student[student.find(' ') + 1:student.find('</a>')]
            count = str(students).count(name + "<")

            if name not in used_names:
                used_names.append(name)
                if name in womens:
                    stat_dict[year]['female'].append((name, count))
                else:
                    stat_dict[year]['male'].append((name, count))

    return stat_dict


def extract_years(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """
    return sorted(stat.keys())


def extract_general(stat, gender=None):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех или для определенного пола.
    Список должен быть отсортирован по убыванию количества.
    """
    name_count_dict = {}

    for year_data in stat.values():
        if gender is None:
            gender_data = (year_data.get('male', []) +
                           year_data.get('female', []))
        else:
            gender_data = year_data.get(gender, [])

        for name, count in gender_data:
            name_count_dict[name] = name_count_dict.get(name, 0) + count

    return sorted(name_count_dict.items(),
                  key=lambda x: (x[1], x[0]), reverse=True)


def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general(stat, gender='male')


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general(stat, gender='female')


def extract_year(stat, year, gender=None):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    name_count_dict = {}

    gender_data = stat[year].get(gender, []) if gender is not None else (
            stat[year].get('male', []) + stat[year].get('female', [])
    )

    for name, count in gender_data:
        for i in range(count):
            name_count_dict[name] = name_count_dict.get(name, 0) + 1

    return sorted(name_count_dict.items(),
                  key=lambda x: (x[1], x[0]), reverse=True)


def extract_year_male(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """

    return extract_year(stat, year, gender='male')


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """

    return extract_year(stat, year, gender='female')


if __name__ == '__main__':
    pass
