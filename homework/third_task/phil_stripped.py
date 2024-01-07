#!/usr/bin/env python3

import urllib.parse
from urllib.request import urlopen
from urllib.parse import unquote
from urllib.parse import quote
import re
import sys


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    url = f"http://ru.wikipedia.org/wiki/{quote(name)}"
    try:
        with urlopen(url) as page:
            content = page.read().decode('utf-8')
            return urllib.parse.unquote(content)
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на
    котором заканчивается содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """
    start_marker = '<div id="mw-content-text"'
    end_marker = '<div id="catlinks" class="catlinks" data-mw="interface">'

    start = page.find(start_marker)
    if start == -1:
        return 0, 0

    end = page.find(end_marker, start)
    if end == -1:
        return 0, 0

    return start, end


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все
    имеющиеся ссылки на другие вики-страницы без повторений и с учётом
    регистра.
    """
    links = set()
    matches = re.finditer(r'<a\s+href=(?:"([^"]*)"|\'([^\']*)\')',
                          page[begin:end], re.IGNORECASE)

    for match in matches:
        link = match.group(1) or match.group(2)

        if link.startswith('/wiki/') and ':' not in link and '#' not in link:
            links.add(unquote(link[6:]))

    return links


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и
    возвращает список переходов, позволяющий добраться из начальной
    статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    visited = set()
    queue = [[start]]

    if start == finish:
        return [start]

    while queue:
        path = queue.pop(0)
        current = path[-1]

        if current in visited:
            continue

        content = get_content(current)
        if content is None:
            continue

        start, end = extract_content(content)
        links = extract_links(content, start, end)

        for link in links:
            if link not in visited:
                new_path = list(path)
                new_path.append(link)
                queue.append(new_path)

                if link == finish:
                    return new_path

        visited.add(current)

    return None


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    start_article = sys.argv[1]
    finish_article = "Философия"

    result = find_chain(start_article, finish_article)

    if result is not None:
        print(result)
    else:
        print(f"Unable to find a chain from {start_article} to "
              f"{finish_article}")


if __name__ == '__main__':
    main()
