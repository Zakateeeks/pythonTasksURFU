import heapq

from PyQt6.QtCore import QTimer


def astar_paint(graph: dict, start: int, widget) -> None:
    """
    Визуализирует алгоритм A* для поиска кратчайшего пути
     на графе с помощью PyQt.

    :param graph: Граф, представленный в виде словаря,
     где ключи - вершины, а значения - словари смежных вершин и весов рёбер.
    :param start: Начальная вершина для алгоритма A*.
    :param widget: Виджет для отображения текущего состояния алгоритма.
    """
    goal = len(graph) - 1
    nocheck_vertex = [(0, start)]
    came_from = {}
    v_score = {vertex: float('infinity') for vertex in graph}
    v_score[start] = 0

    def process_step() -> dict:
        """
        Обрабатывает шаг алгоритма, обновляя
        виджет по мере выполнения алгоритма.
        """
        nonlocal nocheck_vertex, came_from, v_score
        if nocheck_vertex:
            curr_cost, curr_vertex = heapq.heappop(nocheck_vertex)
            if curr_vertex == goal:
                path = []
                while curr_vertex in came_from:
                    path.append(curr_vertex)
                    curr_vertex = came_from[curr_vertex]
                path.append(start)
                path.reverse()
                widget.updateCurrent(current_vertex=curr_vertex,
                                     current_edge=None,
                                     visited_vertices=list(came_from.keys()),
                                     distances=None, current_path=path)

                widget.update()
                return v_score

            for neighbor, weight in graph[curr_vertex].items():
                tentative_v_score = v_score[curr_vertex] + weight
                if tentative_v_score < v_score[neighbor]:
                    came_from[neighbor] = curr_vertex
                    v_score[neighbor] = tentative_v_score
                    f_score = tentative_v_score + heuristic(neighbor, goal)
                    heapq.heappush(nocheck_vertex, (f_score, neighbor))

            widget.updateCurrent(current_vertex=curr_vertex,
                                 visited_vertices=list(came_from.keys()),
                                 current_path=(list(came_from.keys())
                                               + [curr_vertex]))

            QTimer.singleShot(1000, process_step)

    QTimer.singleShot(1000, process_step)


def heuristic(vertex: int, goal: int) -> int:
    """
    Эвристическая функция для алгоритма A*,
     вычисляющая оценку расстояния от текущей вершины до цели.

    :param vertex: Текущая вершина.
    :param goal: Целевая вершина.
    :return: Оценка расстояния от текущей вершины до целевой.
    """
    return abs(vertex - goal)
