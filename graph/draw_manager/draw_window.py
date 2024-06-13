import sys
from functools import partial

from graph.draw_manager.draw_alg.draw_a_star import *
from graph.draw_manager.draw_alg.draw_bell_ford import *
from graph.draw_manager.draw_alg.draw_dijkstra import *
from graph.draw_manager.draw_alg.draw_floyd import *
from graph.draw_manager.draw_graph import *


class GraphWindow(QtWidgets.QMainWindow):
    """
    Главное окно для отображения графа.

    """

    def __init__(self, graph: dict) -> None:
        """
        Инициализирует главное окно.

        :param graph: Граф для отображения.
        """
        super().__init__()
        self.resize(800, 500)
        self.move(300, 200)
        self.setWindowTitle('Graph')

        self.graphWidget = GraphWidget(graph)
        self.setCentralWidget(self.graphWidget)

        self.initUI(graph)

    def initUI(self, graph: dict) -> None:
        """
        Инициализирует пользовательский интерфейс,
         добавляя кнопки для различных алгоритмов.

        :param graph: Граф для отображения и применения алгоритмов.
        """
        toolbar = self.addToolBar('Алгоритмы')
        dijkstra_button = QtWidgets.QPushButton('Дейкстра', self)
        dijkstra_button.clicked.connect(partial(dijkstra_paint,
                                                graph, 0, self.graphWidget))
        toolbar.addWidget(dijkstra_button)

        bellford_button = QtWidgets.QPushButton('Беллмана-Форда', self)
        bellford_button.clicked.connect(partial(bellman_ford_paint,
                                                graph, 0, self.graphWidget))
        toolbar.addWidget(bellford_button)

        floyd_button = QtWidgets.QPushButton('Флойд-Уоршел', self)
        floyd_button.clicked.connect(partial(floyd_warshall_paint,
                                             graph, self.graphWidget))
        toolbar.addWidget(floyd_button)

        a_button = QtWidgets.QPushButton('A star', self)
        a_button.clicked.connect(partial(astar_paint,
                                         graph, 0, self.graphWidget))
        toolbar.addWidget(a_button)


def draw(graph: dict) -> None:
    """
    Отображает заданный граф в приложении.

    :param graph: Граф для отображения.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = GraphWindow(graph)
    window.show()
    sys.exit(app.exec())
