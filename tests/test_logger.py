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


def test_log_message(tmp_path):
    log_message("Test", logging.INFO, get_logger(__name__, tmp_path / "logs"))
    file_name = __name__.replace(".", "_") + ".log"
    file_path = tmp_path / "logs" / file_name
    text = file_path.read_text()
    assert "INFO" in text
    assert f"{__name__}.test_log_message" in text


def test_log_exception(tmp_path):
    log_message(Exception("TEST"), logger=get_logger(__name__, tmp_path / "logs"))
    file_name = __name__.replace(".", "_") + ".log"
    file_path = tmp_path / "logs" / file_name
    text = file_path.read_text()
    assert "ERROR" in text
    assert f"{__name__}.test_log_exception" in text
    assert "Exception: TEST" in text
