import heapq


def astar(graph: dict, start: int) -> dict | None:
    """
     Алгоритм A* для поиска кратчайшего пути

     :param: graph Граф, представленный в виде словаря
     :param: start - Точка старта, вершина от которой начинается поиск

     :return: Словарь, где ключ/значение - вершина/наикратчайший путь
     """

    try:
        nocheck_vertex = []
        key = list(graph.items())
        goal = len(key) - 1
        heapq.heappush(nocheck_vertex, (0, start))
        came_from = {}
        v_score = {vertex: float('infinity') for vertex in graph}
        v_score[start] = 0

        while nocheck_vertex:
            curr_cost, curr_vertex = heapq.heappop(nocheck_vertex)

            if curr_vertex == goal:
                path = []
                while curr_vertex in came_from:
                    path.append(curr_vertex)
                    curr_vertex = came_from[curr_vertex]
                path.append(start)
                path.reverse()
                return v_score

            for neighbor, weight in graph[curr_vertex].items():
                tentative_v_score = v_score[curr_vertex] + weight
                if tentative_v_score < v_score[neighbor]:
                    came_from[neighbor] = curr_vertex
                    v_score[neighbor] = tentative_v_score
                    f_score = tentative_v_score + heuristic(neighbor, goal)
                    heapq.heappush(nocheck_vertex, (f_score, neighbor))

        return None
    except (TypeError, KeyError):
        print(
            "Ошибка: Некорректный формат графа. "
            "Пожалуйста, убедитесь, что граф представлен в "
            "виде словаря с корректными данными.")
        return None


def heuristic(vertex: int, goal: int):
    """
    Функция для подсчета эвристики

    :param: vertex - Текущая вершина
    :param: goal - Конечная вершина

    :return: Эвристика
    """

    return abs(vertex - goal)
