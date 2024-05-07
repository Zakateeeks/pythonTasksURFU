def bellman_ford(graph: dict, src: int) -> dict | None:
    """
    Алгоритм Белмана Форда для поиска кратчайшего пути

    :param graph  Граф (в виде словаря)
    :param src  Точка старта, вершина от которой начинается поиск

    :return: distance  словарь, ключ/значение - вершина/наикратчайший путь
    """

    try:
        count_v = len(graph)
        distance = {vertex: float('infinity') for vertex in graph}
        distance[src] = 0

        for _ in range(count_v - 1):
            for vertex in graph:
                for neighbor, weight in graph[vertex].items():
                    if (distance[vertex] != float("infinity") and distance[vertex]
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
