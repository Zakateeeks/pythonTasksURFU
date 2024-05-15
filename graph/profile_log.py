import logging
import timeit
from memory_profiler import memory_usage

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


def data_usage(func):
    """
    Это декоратор он декорирует
    Этот декоратор используется для проверки памяти и времени
    Все данные записываются в файл с логами

    :param: func - Функция, которую декорируем
    """

    def wrapper(*args, **kwargs):
        mem_before = memory_usage()[0]
        result = func(*args, **kwargs)
        mem_after = memory_usage()[0]

        execution_time = timeit.timeit(lambda: func(*args, **kwargs), number=1000)
        logging.info(f"Function '{func.__name__}' memory usage before:"
                     f" {mem_before} MB")
        logging.info(f"Function '{func.__name__}' memory usage after:"
                     f" {mem_after} MB")
        logging.info(f"Function '{func.__name__}' execution time:"
                     f" {execution_time} seconds")

        return result

    return wrapper
