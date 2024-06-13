from graph.Graph_Find.create_graph import *


def bellman_ford(this_graph: Graph, src: int) -> dict | None:
    """
    Алгоритм Белмана Форда для поиска кратчайшего пути

    Начальное расстояние от начальной вершины до всех остальных
    устанавливается как бесконечность, за исключением начальной вершины,
    расстояние до которой равно нулю.
    Алгоритм проходит по всем рёбрам графа несколько раз и обновляет
    расстояния до каждой вершины, если находит путь, который короче уже
    известного.
    Если успешно найдены кратчайшие пути до всех вершин без отрицательных
    циклов, возвращается словарь, где ключи - вершины, а значения - длины
    кратчайших путей до них от начальной вершины.
    Если обнаружен отрицательный цикл или граф имеет некорректный формат,
    алгоритм возвращает None.


    :param this_graph  Граф
    :param src  Точка старта, вершина от которой начинается поиск

    :return: distance  словарь, ключ/значение - вершина/наикратчайший путь
    """

    try:
        graph = to_dict(this_graph)
        count_v = len(graph)
        distance = {vertex: float('infinity') for vertex in graph}
        distance[src] = 0

        for _ in range(count_v - 1):
            for vertex in graph:
                for neighbor, weight in graph[vertex].items():
                    if (distance[vertex] != float("infinity")
                            and distance[vertex]
                            + weight < distance[neighbor]):
                        distance[neighbor] = distance[vertex] + weight

        for vertex in graph:
            for neighbor, weight in graph[vertex].items():
                if (distance[vertex] != float("infinity") and distance[vertex]
                        + weight < distance[neighbor]):
                    print("Graph contains negative weight cycle")
                    return None

        return distance
    except (TypeError, KeyError):
        print(
            "Ошибка: Некорректный формат графа. Пожалуйста, "
            "убедитесь, что граф представлен "
            "в виде словаря с корректными данными.")
        return None
