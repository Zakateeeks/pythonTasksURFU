from Graph_Find import *
from profile_log import *


@data_usage
def main():
    vertex, count = read_adjacency_matrix("matrix.txt")
    graph = get_graph(vertex, count)

    print(a_star(graph, 0))
    print(bell_ford(graph, 0), "\n", dijkstra(graph, 0), "\n",
          floyd(graph, 0))


if __name__ == "__main__":
    main()
