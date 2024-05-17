import heapq

from graph.Graph_Find.create_graph import *


def dijkstra_search(this_graph: Graph, start: int) -> dict | None:
    """
    Алгоритм Дейкстры для поиска кратчайшего пути

    Поочередно рассматриваем вершины графа, начиная с самой
    близкой к начальной вершине.
    Для каждой вершины мы рассматриваем все её соседние вершины
    и обновляем расстояние до них, если находим более короткий путь.

    :param this_graph  Граф
    :param start  Точка старта, вершина от которой начинается поиск

    :return: distance  словарь, ключ/значение - вершина/наикратчайший путь
    """

    try:
        graph = to_dict(this_graph)
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            current_distance, current_vertex = heapq.heappop(queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in graph[current_vertex].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        return distances
    except (TypeError, KeyError):
        print("Ошибка: Некорректный формат графа."
              " Пожалуйста, убедитесь, что граф представлен "
              "в виде словаря с корректными данными.")
        return None
