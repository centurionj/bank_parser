import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_function_call(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Вызов функции: {func.__name__} с аргументами: {args} и ключевыми аргументами: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Результат работы функции {func.__name__}: {result}")
        return result
    return wrapper