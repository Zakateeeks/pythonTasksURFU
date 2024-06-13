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

Подключение библиотеки происходит через:

```
from Graph_Find import *
```

При этом не стоит забывать импортировать нужные библиотеки. Это можно сделать через ``pip install requirements.txt``

## Профайл ##

В файле `profile_log.py` создаётся декоратор, который при его использовании измеряет время работы функции и затраченную
память.

Результат работы декоратора находится в файле `py_log.log`

