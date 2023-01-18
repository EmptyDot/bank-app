from os import PathLike
from typing import Union


FilePath = Union[PathLike[str], str, None]
AccountArgs = dict[str, Union[int, float]]
