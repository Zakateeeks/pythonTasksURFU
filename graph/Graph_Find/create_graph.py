class Graph:
    """
    Класс отвечает за создание и инициализацию графа.

    Parameters:
    - vertex: список кортежей, содержащих информацию о
    рёбрах графа в формате (source, destination, weight).
    - count_vertex: количество вершин в графе.

    Attributes:
    - adjList: словарь, представляющий список смежности графа.

    Пример использования:

    vertex = [(0, 1, 5), (1, 2, 3), (2, 0, 2)]  # Пример данных о рёбрах графа
    count_vertex = 3  # Количество вершин в графе
    graph = Graph(vertex, count_vertex)  # Инициализация графа
    """

    def __init__(self, vertex: list, count_vertex: int):
        """
        Инициализирует граф с помощью списка рёбер и их весов.

        Создает пустой список смежности и добавляет в него вершины.
        Для каждого ребра из списка vertex добавляет информацию о
        смежной вершине и весе ребра.


        :param vertex: список кортежей, содержащих информацию о рёбрах графа
        в формате (source, destination, weight).
        :param count_vertex: количество вершин в графе.

        """

        self.adjList = dict()

        for i in range(count_vertex):
            self.adjList[i] = dict()

        for (src, dest, weight) in vertex:
            self.adjList[src][dest] = weight


def get_graph(vertex: list, count_vertex: int) -> Graph:
    """
    Создает объект графа и возвращает его список смежности.

    :param vertex: список кортежей, содержащих информацию
     о рёбрах графа в формате (source, destination, weight).
    :param count_vertex: количество вершин в графе.

    :return: dict: список смежности графа.

    """

    graph = Graph(vertex, count_vertex)
    return graph


def set_graph() -> tuple:
    """
    Запрашивает у пользователя информацию о графе.

    Пользователь вводит количество вершин графа и
    для каждой вершины вводит информацию
    о смежных вершинах и весе рёбер.

    :return: tuple: кортеж содержащий список рёбер графа и количество вершин.

    """

    try:
        count_vertex = int(input("Введите количество вершин графа: "))
        vertex = []

        print("Хорошо! Теперь введите вершину, смежную вершину и вес ребра")
        for i in range(count_vertex):
            # Обрабатываем исключение для случая,
            # если пользователь вводит некорректные данные
            try:
                vertex.append(tuple(int(x) for x in input().split()))
            except ValueError:
                print("Ошибка: Введите корректные данные в формате: "
                      "<source> <destination> <weight>")
                return set_graph()

        return vertex, count_vertex
    except ValueError:
        print("Ошибка: Введите корректное число вершин.")
        return set_graph()


def to_dict(graph: Graph) -> dict:
    """
    Переводит граф в словарь.

    :param graph: переменная типа Graph
    :return: dict: словарь, содержащий вершины графа, смежные вершины и вес

    """
    return graph.adjList


def read_adjacency_matrix(filename: str) -> tuple | int:
    """
    Читает матрицу смежности из файла и преобразует ее в список рёбер графа.

    :param filename: имя файла, содержащего матрицу смежности графа.
    :return: tuple: кортеж содержащий список рёбер графа и количество вершин.
    """

    try:
        with open(filename, 'r') as file:
            adjacency_matrix = []
            for line in file:
                row = list(map(int, line.strip().split()))
                adjacency_matrix.append(row)

        count_vertex = len(adjacency_matrix)
        vertex = []

        for i in range(count_vertex):
            for j in range(count_vertex):
                if adjacency_matrix[i][j] != 0:
                    vertex.append((i, j, adjacency_matrix[i][j]))

        return vertex, count_vertex
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None, None
    except (ValueError, IndexError):
        print(
            f"Ошибка: Некорректный формат содержимого файла '{filename}'."
            f" Пожалуйста, убедитесь, что "
            f"матрица смежности записана корректно.")
        return None, None
