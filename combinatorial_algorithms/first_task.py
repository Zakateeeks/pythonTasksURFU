'''
Ввод	in.txt
Вывод	out.txt

Определить, является ли данный граф ацикличным.

Метод решения: Поиск в ширину.

Формат ввода
Первая строка содержит единственное число N — количество вершин в графе.
Далее построчно расположена матрица смежности размерности N x N.

Формат вывода
Для ацикличного графа файл ответа должен содержать единственный символ: "A"(латинское).
Если в графе есть цикл, то в первой строке "N", во второй упорядоченный по возрастанию номеров список вершин,
входящих в первый найденный цикл. Нумерация вершин графа начинается с единицы.
'''
from queue import Queue


def read_graph(filename) -> dict:
    graph = {}
    with open(filename, 'r') as file:
        size = int(file.readline())
        for i in range(1, size + 1):
            vertex = [int(x) for x in file.readline().split()]
            graph[i] = [j + 1 for j, val in enumerate(vertex) if val]
    return graph


def check_graph(graph, visited):
    queue = Queue()
    queue.put(1)
    steps = [-1] * len(graph)

    while not queue.empty():
        current = queue.get()

        if current in visited:
            return cycle_graph(steps, current)

        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.put(neighbor)
                if steps[neighbor - 1] != -1:
                    steps[neighbor - 1] = ((steps[neighbor - 1], current))
                    return cycle_graph(steps, neighbor)
                else:
                    steps[neighbor - 1] = current

            visited.add(current)

    return None


def cycle_graph(steps, neighbor):
    first_part = {neighbor}
    current = steps[neighbor - 1][0]
    while current != -1:
        first_part.add(current)
        current = steps[current - 1]

    second_part = set()
    current = steps[neighbor - 1][1]

    first_same_node = True
    start_of_cycle = -1

    while current != -1:
        if current in first_part and first_same_node:
            first_same_node = False
            start_of_cycle = current
            continue
        second_part.add(current)
        current = steps[current - 1]

    cycle = first_part ^ second_part
    cycle.add(start_of_cycle)

    return sorted(cycle)


def out(result):
    with open("out.txt", 'w') as file:
        if result is None:
            file.write("A")
        else:
            res_str = str(result)[1:-1].replace(',','')
            file.write(f"N\n{res_str}\n")


def main() -> None:
    graph = read_graph("in.txt")
    visited = set()
    result = check_graph(graph, visited)
    out(result)


if __name__ == "__main__":
    main()
