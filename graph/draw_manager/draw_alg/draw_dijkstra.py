import heapq

from PyQt6.QtCore import QTimer


def dijkstra_paint(graph: dict, start: int, widget) -> None:
    """
    Визуализирует алгоритм Дейкстры для поиска кратчайшего пути
     на графе с помощью PyQt.

    :param graph: Граф, представленный в виде словаря, где ключи - вершины,
     а значения - словари смежных вершин и весов рёбер.
    :param start: Начальная вершина для алгоритма Дейкстры.
    :param widget: Виджет для отображения текущего состояния алгоритма.
    """
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    queue = [(0, start)]
    visited = set()
    came_from = {}

    def process_queue() -> None:
        """
        Обрабатывает очередь вершин для посещения,
         обновляя виджет по мере выполнения алгоритма.
        """
        if not queue:
            final_path = []
            current_vertex = len(graph) - 1
            while current_vertex in came_from:
                final_path.append(current_vertex)
                current_vertex = came_from[current_vertex]
            final_path.append(start)
            final_path.reverse()

            widget.updateCurrent(visited_vertices=visited,
                                 current_path=final_path)
            return

        current_distance, current_vertex = heapq.heappop(queue)

        if current_vertex in visited:
            QTimer.singleShot(500, process_queue)
            return

        visited.add(current_vertex)
        widget.updateCurrent(current_vertex=current_vertex,
                             visited_vertices=visited)

        edges_to_process = []
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                edges_to_process.append((current_vertex, neighbor))
                came_from[neighbor] = current_vertex

        def process_edges() -> None:
            """
            Обрабатывает рёбра текущей вершины,
             обновляя виджет по мере выполнения алгоритма.
            """
            if not edges_to_process:
                widget.update()
                QTimer.singleShot(500, process_queue)
                return

            current_edge = edges_to_process.pop(0)
            widget.updateCurrent(current_vertex=current_vertex,
                                 current_edge=current_edge,
                                 visited_vertices=visited)
            widget.update()
            QTimer.singleShot(500, process_edges)

        QTimer.singleShot(500, process_edges)

    QTimer.singleShot(500, process_queue)
