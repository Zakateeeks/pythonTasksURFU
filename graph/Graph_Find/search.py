from graph.Graph_Find.search_alg import *


def dijkstra(graph: dict, start: int) -> dict | None:
    """
    Алгоритм Дейкстры для поиска кратчайшего пути

    :param graph  Граф (в виде словаря)
    :param start  Точка старта, вершина от которой начинается поиск

    :return: distance  словарь, ключ/значение - вершина/наикратчайший путь
    """
    return dijkstra_search(graph, start)


def bell_ford(graph: dict, start: int) -> dict | None:
    """
    Алгоритм Белмана Форда для поиска кратчайшего пути

    :param graph  Граф (в виде словаря)
    :param start  Точка старта, вершина от которой начинается поиск

    :return: distance  словарь, ключ/значение - вершина/наикратчайший путь
    """
    return bellman_ford(graph, start)


def floyd(graph: dict, start: int) -> dict | None:
    """
    Алгоритм Флойда-Уоршелла для поиска кратчайшего пути

    :param: graph Граф, представленный в виде словаря
    :param: start - Точка старта, вершина от которой начинается поиск

    :return: Словарь, где ключ/значение - вершина/наикратчайший путь
    """
    floyd_res = floyd_warshall(graph)[start]
    floyd_res[start] = 0
    return floyd_res


def a_star(graph: dict, start: int) -> dict | None:
    """
    Алгоритм A* для поиска кратчайшего пути

    :param: graph Граф, представленный в виде словаря
    :param: start - Точка старта, вершина от которой начинается поиск

    :return: Словарь, где ключ/значение - вершина/наикратчайший путь
    """
    return astar(graph, start)
