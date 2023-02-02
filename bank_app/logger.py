import functools
import inspect
import logging
import os.path
from typing import Union, Callable, Any, Iterable, Type


def get_logger(
    name: str = "bankapp", parent_dir_path: str = "bank_app/logs"
) -> logging.Logger:
    """
    Get a logger
    :param name: Name referring to the logger. Recommended value is the __name__ of the module for separate files. Leave default for one file.
    :param parent_dir_path: Parent directory of the logs
    :return: A logger with the specified name, creating it if necessary.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not os.path.isdir(parent_dir_path):
        os.mkdir(parent_dir_path)

    file_name = name.replace(".", "_")
    log_file_path = f"{parent_dir_path}/{file_name}.log"

    handler = logging.FileHandler(log_file_path, mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


DEFAULT_LOGGER = get_logger()

def get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
            return cls
    return None

def log_message(
    message: Union[str, Exception],
    func: Callable,
    level: int = logging.ERROR,
    logger: logging.Logger = DEFAULT_LOGGER,
    stack_level: int = 0,
):

    stack = inspect.stack()
    calling_frame = stack[1]
    module_name = inspect.getmodule(calling_frame[0]).__name__
    function_name = calling_frame[3]
    class_name = ""
    if "self" in calling_frame[0].f_locals:
        class_name = calling_frame[0].f_locals["self"].__class__.__name__
    if isinstance(message, str):
        logger.log(
            level=level,
            msg=f"{module_name}.{func.__name__} - {message}",
        )
    if isinstance(message, Exception):
        logger.log(
            level=level,
            msg=f"{module_name}.{class_name + '.' if class_name else ''}{function_name}: {message.__class__.__name__}: {message}",
        )


def log_exception(
    expected_exc: Type[BaseException] | Iterable[Type[BaseException]] = Exception,
    logger: logging.Logger = DEFAULT_LOGGER,
    default_return: Any = False,
    raise_exc: bool = False,
    stack_level: int = 1,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                value = func(*args, **kwargs)
            except* expected_exc as eg:
                for e in eg.exceptions:
                    logger.log(
                        level=logging.ERROR,
                        msg=f"{module_name}.{class_name + '.' if class_name else ''}{function_name}: {e.__class__.__name__}: {e}",
                    )

                if raise_exc:
                    raise eg
            else:
                return value
            finally:
                return default_return

        return wrapper

    return decorator



