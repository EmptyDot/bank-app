from __future__ import annotations

import inspect
import logging
import os.path
from typing import Optional


def get_logger(module_name: str, logging_level: int | str = logging.WARNING) -> logging.Logger:
    """
    Initialize a new logger
    :param module_name: Name referring to the logger. Recommended value is __name__.
    :param logging_level: Set the logging level of this logger. logging_level must be an int or a str.
    :return: A logger with the specified name, creating it if necessary.
    """

    logger = logging.getLogger(module_name)
    logger.setLevel(logging_level)

    if not os.path.isdir("logs"):
        if os.path.exists("logs"):
            log_abs_path = os.path.dirname(__file__) + r"\logs"
            raise FileExistsError(f"Can't create a directory, file 'logs' already exists. {log_abs_path}")
        os.mkdir("logs")

    file_name = module_name.replace(".", "_")
    log_file_path = f"logs/{file_name}.log"
    handler = logging.FileHandler(log_file_path, mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info(log_message(f"Create logger for {module_name}"))
    return logger


def log_message(message: Optional[str] = ""):
    stack = inspect.stack()
    calling_frame = stack[1]
    function_name = calling_frame[3]
    class_name = ''
    if 'self' in calling_frame[0].f_locals:
        class_name = calling_frame[0].f_locals['self'].__class__.__name__
    return f"{class_name + '.' if class_name else ''}{function_name}: {message}"






