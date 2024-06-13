import math

from PyQt6 import QtWidgets, QtGui, QtCore


class GraphWidget(QtWidgets.QWidget):
    """
     Класс виджета для визуализации графа с помощью PyQt6.

     :param graph: Словарь, представляющий граф, где ключи - это вершины,
     а значения - словари соседей и их весов.
     :param node_positions: Словарь с координатами вершин на виджете.
     :param edges: Список рёбер графа, содержащий вершины и веса рёбер.
     :param current_step: Текущий шаг анимации.
     :param current_vertex: Текущая вершина, используемая
     для визуализации текущего состояния.
     :param current_edge: Текущее ребро, используемое
      для визуализации текущего состояния.
     :param visited_vertices: Множество посещённых вершин.
     :param unvisited_vertices: Множество непосещённых вершин.
     :param distances: Матрица расстояний между вершинами.
     :param current_path: Текущий путь для визуализации.
     :param timer: Таймер для обновления анимации.
     """

    def __init__(self, graph: dict, parent=None) -> None:
        """
        Инициализация виджета графа.

        :param graph: Словарь, представляющий граф.
        :param parent: Родительский виджет.
        """
        super().__init__(parent)
        self.graph = graph
        self.node_positions = {}
        self.edges = []
        self.current_step = 0
        self.current_vertex = None
        self.current_edge = None
        self.visited_vertices = set()
        self.unvisited_vertices = set(graph.keys())
        self.distances = None
        self.initGraph()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.nextStep)
        self.timer.start(30)
        self.current_path = None

    def initGraph(self) -> None:
        """
         Инициализация позиций вершин и рёбер графа для визуализации.
        """
        padding = 20
        width = self.width()
        height = self.height()
        num_nodes = len(self.graph)
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - padding
        angle_step = 360 / num_nodes
        for i, node in enumerate(self.graph.keys()):
            angle = angle_step * i
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            self.node_positions[node] = (x, y)
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                if neighbor in self.node_positions:
                    self.edges.append((node, neighbor, weight))

    def nextStep(self) -> None:
        """
         Обновление шага анимации.
        """
        self.current_step += 1
        self.update()

    def paintEvent(self, event) -> None:
        """
        Отрисовка виджета.

        :param event: Событие отрисовки.
        """
        painter = QtGui.QPainter(self)
        self.drawGraph(painter)

        if self.current_path:
            painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.red, 3))
            for i in range(len(self.current_path) - 1):
                node1 = self.current_path[i]
                node2 = self.current_path[i + 1]
                if (node1 in self.node_positions and
                        node2 in self.node_positions):
                    x1, y1 = self.node_positions[node1]
                    x2, y2 = self.node_positions[node2]
                    painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        self.drawVisitedTable(painter)

    def drawGraph(self, painter) -> None:
        """
        Отрисовка графа.

        :param painter: Объект для отрисовки.
        """
        node_radius = 10
        original_font = painter.font()

        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)

        for node, (x, y) in self.node_positions.items():
            if node in self.visited_vertices:
                painter.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.blue))
            else:
                painter.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.green))
            painter.drawEllipse(QtCore.QPoint(int(x), int(y)),
                                node_radius, node_radius)
            painter.drawText(int(x) - node_radius,
                             int(y) - node_radius, 2 * node_radius,
                             2 * node_radius,
                             QtCore.Qt.AlignmentFlag.AlignCenter, str(node))
        painter.setFont(original_font)
        for node, neighbor, weight in self.edges:
            x1, y1 = self.node_positions[node]
            x2, y2 = self.node_positions[neighbor]
            if ((node, neighbor) == self.current_edge
                    or (neighbor, node) == self.current_edge):
                painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.red, 5))
            else:
                painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 2))
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            original_pen = painter.pen()
            painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.red))
            painter.drawText(int(mid_x), int(mid_y), str(weight))
            painter.setPen(original_pen)

        if self.distances:
            self.drawDistances(painter)

    def drawDistances(self, painter) -> None:
        """
        Отрисовка расстояний.

        :param painter: Объект для отрисовки.
        """
        table_width = self.width() * 0.3
        table_height = self.height() * 0.3
        start_x = self.width() - table_width - 20
        start_y = 20
        cell_width = table_width / len(self.distances)
        cell_height = table_height / len(self.distances)

        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black))
        for i in range(len(self.distances)):
            for j in range(len(self.distances)):
                rect = QtCore.QRect(start_x + j * cell_width,
                                    start_y + i * cell_height,
                                    cell_width, cell_height)
                painter.drawRect(rect)
                painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter,
                                 str(self.distances[i][j]))

    def drawVisitedTable(self, painter) -> None:
        """
        Отрисовка таблицы посещённых и непосещённых вершин.

        :param painter: Объект для отрисовки.
        """
        indent = 20
        table_width = 150
        table_height = self.height() - 30
        start_x = self.width() - table_width - indent
        start_y = self.height() - table_height - indent

        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))
        painter.drawRect(start_x, start_y, table_width, table_height)

        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)

        cell_height = table_height // (
                max(len(self.visited_vertices),
                    len(self.graph) - len(self.visited_vertices)) + 20)

        painter.drawText(start_x, start_y, table_width, cell_height,
                         QtCore.Qt.AlignmentFlag.AlignCenter, "Visited")
        painter.drawText(start_x, start_y + table_height // 2,
                         table_width, cell_height,
                         QtCore.Qt.AlignmentFlag.AlignCenter, "Unvisited")

        visited_y = start_y + cell_height
        unvisited_y = start_y + table_height // 2 + cell_height

        for vertex in self.visited_vertices:
            painter.drawText(start_x, visited_y, table_width, cell_height,
                             QtCore.Qt.AlignmentFlag.AlignCenter, str(vertex))
            visited_y += cell_height + 5

        for vertex in self.unvisited_vertices:
            painter.drawText(start_x, unvisited_y, table_width, cell_height,
                             QtCore.Qt.AlignmentFlag.AlignCenter, str(vertex))
            unvisited_y += cell_height + 5

    def updateCurrent(self, current_vertex=None, current_edge=None,
                      visited_vertices=None, distances=None,
                      current_path=None) -> None:
        """
        Обновление текущих состояний графа и перерисовка виджета.

        :param current_vertex: Текущая вершина.
        :param current_edge: Текущее ребро.
        :param visited_vertices: Множество посещённых вершин.
        :param distances: Матрица расстояний между вершинами.
        :param current_path: Текущий путь для визуализации.
        """
        self.current_vertex = current_vertex
        self.current_edge = current_edge
        if visited_vertices is not None:
            self.visited_vertices = set(visited_vertices)
            self.unvisited_vertices = (set(self.graph.keys()) -
                                       self.visited_vertices)
        if distances is not None:
            self.distances = distances
        self.current_path = current_path
        self.update()
