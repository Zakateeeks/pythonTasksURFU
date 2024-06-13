from tabulate import tabulate

from Graph_Find import *
from graph.draw_manager.draw_window import *
from graph.logger.profile_log import *


def check_func() -> None:
    """
    Функция для проверки алгоритмов на скорость и производительность
    """
    vertex, count = read_adjacency_matrix("resources/fourth_matrix.txt")
    graph = get_graph(vertex, count)

    @time_check
    def a_star_time():
        a_star(graph, 0)

    @data_usage
    def a_star_data():
        a_star(graph, 0)

    @time_check
    def bellma_ford_time():
        bell_ford(graph, 0)

    @data_usage
    def bellma_ford_data():
        bell_ford(graph, 0)

    @time_check
    def dijkstra_time():
        dijkstra(graph, 0)

    @data_usage
    def dijkstra_data():
        dijkstra(graph, 0)

    @time_check
    def floyd_time():
        floyd(graph, 0)

    @data_usage
    def floyd_data():
        floyd(graph, 0)

    a_star_time()
    a_star_data()
    bellma_ford_time()
    bellma_ford_data()
    dijkstra_time()
    dijkstra_data()
    floyd_time()
    floyd_data()
    results = []

    for func_name in time_results.keys():
        time_data = time_results[func_name]
        results.append((func_name, *time_data))

    headers = ['Function', 'Min Time (s)', 'Max Time (s)',
               'Avg Time (s)']

    print(tabulate(results, headers=headers, tablefmt='grid'))

    headers = ['Function', 'Max Memory (MB)', 'Min Memory (MB)',
               'Avg Memory (MB)']
    results = []
    for func_name in memory_results.keys():
        memory_data = memory_results[func_name]
        results.append((func_name, *memory_data))
    print(tabulate(results, headers=headers, tablefmt='grid'))


def main():
    vertex, count = read_adjacency_matrix("resources/fourth_matrix.txt")
    graph = get_graph(vertex, count)
    draw(to_dict(graph))


if __name__ == "__main__":
    main()
