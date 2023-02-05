import logging
import os.path

import pytest

from bank_app.logger import *


def test_get_logger(tmp_path):
    logger = get_logger("LOGGER.TEST", tmp_path)
    assert os.path.exists(tmp_path / "LOGGER_TEST.log")
    assert isinstance(logger, logging.Logger)


def test_get_logger_file_exists_error(tmp_path):

    open(tmp_path / "logs", "a").close()

    with pytest.raises(FileExistsError):
        get_logger("LOGGER.TEST", tmp_path / "logs")


def test_log_exc():
    @log_exc(logger=logging.getLogger())
    def f():
        return True
    assert f() is True


def test_log_exc_error_catch():
    @log_exc(exc=ValueError, logger=logging.getLogger())
    def f():
        raise ValueError("test")
    assert f() is None


def test_log_exc_error_catch_return():
    @log_exc(exc=ValueError, return_value="foo", logger=logging.getLogger())
    def f():
        raise ValueError("test")
    assert f() == "foo"


def test_log_exc_wrong_error():
    with pytest.raises(ValueError):
        @log_exc(exc=AttributeError, logger=logging.getLogger())
        def f():
            raise ValueError("test")

        f()


def test_log_exc_error_raise():
    with pytest.raises(ValueError):
        @log_exc(exc=ValueError, raise_exc=True, logger=logging.getLogger())
        def f():
            raise ValueError("test")

        f()


def test_log_exc_error_multiple():
    @log_exc(exc=(ValueError, TypeError), logger=logging.getLogger())
    def f():
        raise ValueError("test")

    assert f() is None


def test_log_exc_wrong_error_multiple():
    with pytest.raises(ValueError):
        @log_exc(exc=(AttributeError, TypeError), logger=logging.getLogger())
        def f():
            raise ValueError("test")

        f()


def test_log_exc_info_msg(caplog):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @log_exc(logger=logger)
    def f():
        return True

    assert f() is True
    assert f"Calling {f.__qualname__}" in caplog.text


def test_log_exc_error_msg_catch(caplog):
    @log_exc(exc=ValueError, logger=logging.getLogger())
    def f():
        raise ValueError("test")

    assert f() is None
    assert f"{ValueError().__class__.__name__}: {ValueError('test')}" in caplog.text


def test_log_exc_error_msg_raise(tmp_path, caplog):
    with pytest.raises(ValueError):

        @log_exc(exc=ValueError, raise_exc=True, logger=logging.getLogger())
        def f():
            raise ValueError("test")

        f()

    assert f"{ValueError().__class__.__name__}: {ValueError('test')}" in caplog.text


