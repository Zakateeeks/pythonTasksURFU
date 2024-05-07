# Алгоритмы поиска наикратчайшего пути в графе #

## Использование ##
 - Декоратор для измерения ресурсов
```
 from profile_log import *
 
 @data_usage
 def function():
 ```
- Создание Графа
  - Через матрицу смежности
  ```
    vertex, count = read_adjacency_matrix("matrix.txt")
    graph = get_graph(vertex, count)
  ```
  - Через ввод с клавиатуры
  ```
    vertex, count = set_graph()
    graph = get_graph(vertex, count)
  ```
- Функции поиска
  - Алгоритм Дейкстры
  ```
    dijkstra(graph, start)
  ```
  - Алгоритм Белмана Форда
  ```
    bell_ford(graph, start)
  ```
  - Алгоритм Флойда-Уоршелла
  ```
    floyd(graph, start)
  ```
  - Алгоритм А*
  ```
    a_star(graph, start)
  ```

## Подключение библиотеки ##
Тасс, pip install не будет, потому что это надо заливать 
на PyPi а я не хочу ((

Подключение библиотеки происходит через:
```
from Graph_Find import *
```

## Допы ##
- [ ] Таска 1
- [ ] Таска 2 