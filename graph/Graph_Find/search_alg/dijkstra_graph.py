import heapq


def dijkstra_search(graph: dict, start: int) -> dict | None:
    """
    Алгоритм Дейкстры для поиска кратчайшего пути

    :param graph  Граф (в виде словаря)
    :param start  Точка старта, вершина от которой начинается поиск

    :return: distance  словарь, ключ/значение - вершина/наикратчайший путь
    """

    try:
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