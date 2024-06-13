from PyQt6.QtCore import QTimer


def bellman_ford_paint(graph: dict, start: int, widget) -> None:
    """
    Визуализирует алгоритм Беллмана-Форда для поиска
     кратчайшего пути на графе с помощью PyQt.

    :param graph: Граф, представленный в виде словаря,
     где ключи - вершины, а значения - словари смежных вершин и весов рёбер.
    :param start: Начальная вершина для алгоритма Беллмана-Форда.
    :param widget: Виджет для отображения текущего состояния алгоритма.
    """
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    vertices = list(graph.keys())
    visited = set()

    edge_list = []
    for u in graph:
        for v, weight in graph[u].items():
            edge_list.append((u, v, weight))

    def process_edges(edges: list, iteration: int) -> None:
        """
        Обрабатывает рёбра графа, обновляя виджет
         по мере выполнения алгоритма.

        :param edges: Список рёбер для обработки.
        :param iteration: Текущая итерация алгоритма.
        """
        nonlocal u, v, weight

        if iteration >= len(vertices) - 1:
            if edge_list:
                check_negative_cycle()
            final_path()
            return

        if not edges:
            QTimer.singleShot(300,
                              lambda: process_edges(edge_list, iteration + 1))
            return

        u, v, weight = edges.pop(0)
        if distances[u] + weight < distances[v]:
            distances[v] = distances[u] + weight
            visited.add(u)
            visited.add(v)
            widget.updateCurrent(current_vertex=v,
                                 current_edge=(u, v),
                                 visited_vertices=visited)

        QTimer.singleShot(300, lambda: process_edges(edges, iteration))

    def check_negative_cycle() -> None:
        """
        Проверяет наличие отрицательных циклов в графе.
        """
        nonlocal edge_list, u, v, weight
        negative_cycle = False
        for u, v, weight in edge_list:
            if distances[u] + weight < distances[v]:
                negative_cycle = True
                break
        widget.updateCurrent(negative_cycle=negative_cycle)

    def final_path() -> None:
        """
        Определяет окончательный путь после завершения алгоритма.
        """
        nonlocal u, v, weight
        edg_list = []
        for u in graph:
            for v, weight in graph[u].items():
                edg_list.append((u, v, weight))
        final_pat = []
        current_vertex = len(graph) - 1
        while current_vertex != start:
            final_pat.append(current_vertex)
            for u, v, weight in edg_list:
                if (v == current_vertex and
                        distances[current_vertex] == distances[u] + weight):
                    current_vertex = u
                    break
        final_pat.append(start)
        final_pat.reverse()

        widget.updateCurrent(visited_vertices=visited, current_path=final_pat)

    QTimer.singleShot(300, lambda: process_edges(edge_list, 0))
