from __future__ import annotations

import functools
import logging
import pathlib
import sys
import tempfile
import warnings
from os import PathLike
from typing import Callable, Any, Iterable, Type


def get_logger(
    name: str = "bankapp", parent_dir_path: PathLike[str] = "logs"
) -> logging.Logger:
    """
    Get a logger
    :param name: Name referring to the logger. Recommended value is the __name__ of the module for separate files. Leave default for one file.
    :param parent_dir_path: Parent directory of the logs
    :return: A logger with the specified name, creating it if necessary.
    """

    path = pathlib.Path(parent_dir_path)
    path.mkdir(parents=True, exist_ok=True)
    file_name = name.replace(".", "_") + ".log"
    log_file_path = path / file_name

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_path, mode="w")
    formatter = logging.Formatter(
        "%(levelname)s - %(module)s - line %(lineno)d - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


DEFAULT_LOGGER = get_logger()


def log_exc(
    _func: Callable | None = None,
    *,
    exc: Type[BaseException] | Iterable[Type[BaseException]] = Exception,
    logger: logging.Logger | None = DEFAULT_LOGGER,
    raise_exc: bool = False,
    return_value: Any = None,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"Calling {func.__qualname__}", stacklevel=2)
            try:
                value = func(*args, **kwargs)
                return value
            except Exception as e:
                logger.error(f"{e.__class__.__name__}: {e}", stacklevel=2)
                if raise_exc:
                    raise e
                if isinstance(exc, Iterable):
                    if not any(isinstance(e, expected) for expected in exc):
                        raise e
                elif issubclass(exc, Exception):
                    if not isinstance(e, exc):
                        raise e

            return return_value

        return wrapper

    return decorator if _func is None else decorator(_func)





