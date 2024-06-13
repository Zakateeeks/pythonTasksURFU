from PyQt6.QtCore import QTimer


def floyd_warshall_paint(graph: dict, widget) -> None:
    """
    Визуализирует алгоритм Флойда-Уоршелла для поиска
     кратчайших путей на графе с помощью PyQt.

    :param graph: Граф, представленный в виде словаря,
     где ключи - вершины, а значения - словари смежных вершин и весов рёбер.
    :param widget: Виджет для отображения текущего состояния алгоритма.
    """
    n = len(graph)
    dist = [[float('infinity')] * n for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if u == v:
                dist[u][v] = 0
            elif v in graph[u]:
                dist[u][v] = graph[u][v]

    def process_step() -> None:
        """
        Обрабатывает шаг алгоритма, обновляя виджет
         по мере выполнения алгоритма.
        """
        nonlocal k, i, j
        if k < n:
            if i < n:
                if j < n:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        print(f"Обновление dist[{i}][{j}] через вершину {k}")
                        widget.updateCurrent(current_vertex=k,
                                             current_edge=(i, j),
                                             visited_vertices={i, j, k})
                    j += 1
                else:
                    j = 0
                    i += 1
            else:
                i = 0
                k += 1
            widget.update()
            if k < n:
                QTimer.singleShot(50, process_step)

    k, i, j = 0, 0, 0
    QTimer.singleShot(50, process_step)
