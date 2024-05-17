import logging
import timeit

import colorlog
from memory_profiler import memory_usage

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

logging.getLogger().handlers = []


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

        logger.info(f"Function '{func.__name__}' memory usage :"
                     f" {mem_after - mem_before} MB")

        return result

    return wrapper


def time_check(func):
    def wrapper(*args, **kwargs):
        execution_time = timeit.timeit(lambda: func(*args, **kwargs), number=1)
        logger.info(f"Function '{func.__name__}' execution time:"
                     f" {execution_time} seconds")

        return execution_time

    return wrapper
