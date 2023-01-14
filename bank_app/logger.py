from __future__ import annotations

import inspect
import logging
import os.path


def get_logger(name: str = "bankapp") -> logging.Logger:
    """
    Get a logger
    :param name: Name referring to the logger. Recommended value is the __name__ of the module for separate files. Leave default for one file.
    :return: A logger with the specified name, creating it if necessary.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not os.path.isdir("logs"):
        if os.path.exists("logs"):
            log_abs_path = os.path.dirname(__file__) + r"\logs"
            raise FileExistsError(
                f"Can't create a directory, file 'logs' already exists. {log_abs_path}"
            )
        os.mkdir("logs")

    file_name = name.replace(".", "_")
    log_file_path = f"bank_app/logs/{file_name}.log"
    handler = logging.FileHandler(log_file_path, mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


DEFAULT_LOGGER = get_logger()


def log_message(message: str, level: int, logger: logging.Logger = DEFAULT_LOGGER):
    stack = inspect.stack()
    calling_frame = stack[1]
    module_name = inspect.getmodule(calling_frame[0]).__name__
    function_name = calling_frame[3]
    class_name = ""
    if "self" in calling_frame[0].f_locals:
        class_name = calling_frame[0].f_locals["self"].__class__.__name__
    logger.log(
        level=level,
        msg=f"{module_name}.{class_name + '.' if class_name else ''}{function_name}: {message}",
    )


def log_exception(exc: Exception, logger: logging.Logger = DEFAULT_LOGGER):
    log_message(f"{type(exc).__name__}: {exc}", logging.ERROR, logger)
