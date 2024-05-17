from Graph_Find import *
from graph.logger.profile_log import *


def main():
    vertex, count = read_adjacency_matrix("resources/second_matrix.txt")
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


if __name__ == "__main__":
    main()
