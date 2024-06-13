import logging
import statistics
import timeit

import colorlog
from memory_profiler import memory_usage

# Настройка логгера
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(message)s',
    log_colors={
        'DEBUG': 'bold_blue',
        'INFO': 'bold_green',
        'WARNING': 'bold_yellow',
        'ERROR': 'bold_red',
        'CRITICAL': 'bold_purple'
    }
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

time_results = {}
memory_results = {}


def data_usage(func):
    """
    Декоратор для измерения использования памяти функцией.

    :param func: Функция, для которой измеряется использование памяти.
    :return: Результат выполнения функции.
    """

    def wrapper(*args, **kwargs):
        memory_usages = []
        result = 0
        for _ in range(100):
            mem_before = memory_usage()[0]
            result = func(*args, **kwargs)
            mem_after = memory_usage()[0]
            memory_usages.append(mem_after - mem_before)

        max_memory = max(memory_usages)
        min_memory = min(memory_usages)
        avg_memory = statistics.mean(memory_usages)

        memory_results[func.__name__] = (max_memory, min_memory, avg_memory)

        logger.info(f"Function '{func.__name__}' memory usage over 100 runs: "
                    f"Max: {max_memory} MB, Min: {min_memory} MB,"
                    f" Avg: {avg_memory} MB")

        return result

    return wrapper


def time_check(func):
    """
    Декоратор для измерения времени выполнения функции.

    :param func: Функция, для которой измеряется время выполнения.
    :return: Минимальное, максимальное и среднее время выполнения функции.
    """

    def wrapper(*args, **kwargs):
        execution_times = []
        for _ in range(100):
            execution_time = timeit.timeit(lambda: func(*args, **kwargs),
                                           number=1)
            execution_times.append(execution_time)

        min_time = min(execution_times)
        max_time = max(execution_times)
        avg_time = statistics.mean(execution_times)

        time_results[func.__name__] = (min_time, max_time, avg_time)

        logger.info(f"Function '{func.__name__}' execution times over"
                    f" 100 runs: "
                    f"Min time: {min_time} seconds, Max time:"
                    f" {max_time} seconds, Avg time: {avg_time} seconds")

        return min_time, max_time, avg_time

    return wrapper
