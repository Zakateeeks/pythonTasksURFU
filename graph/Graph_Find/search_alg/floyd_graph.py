from graph.Graph_Find.create_graph import *


def floyd_warshall(this_graph: Graph) -> dict | None:
    """
    Алгоритм Флойда-Уоршелла для поиска кратчайшего пути

    Заполняется матрица начальными значениями из графа.
    Происходит обновление матрицы путём последовательного рассмотрения
    всех троек вершин. Если обнаруживается путь между вершинами через
    третью вершину, который короче, чем текущий наилучший путь, этот
    путь обновляется.

    :param: this_graph Граф

    :return: Словарь, где ключ/значение - вершина/наикратчайший путь
    """

    try:
        graph = to_dict(this_graph)
        n = len(graph)
        dist = [[float('infinity')] * n for _ in range(n)]

        for u in graph:
            for v in graph[u]:
                dist[u][v] = graph[u][v]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        result = {}
        for i in range(n):
            result[i] = {}
            for j in range(n):
                result[i][j] = dist[i][j]

        return result
    except (TypeError, IndexError):
        print(
            "Ошибка: Некорректный формат графа. Пожалуйста, убедитесь, "
            "что граф представлен в виде словаря с корректными данными.")
        return None
