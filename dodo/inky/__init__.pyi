# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring, unused-argument
from typing import Any

from PIL import Image

class InkyPHAT:
    WIDTH: int
    HEIGHT: int
    WHITE: int
    BLACK: int
    RED: int
    YELLOW: int
    def __init__(self, colour: str): ...
    def set_border(self, colour: int) -> None: ...
    def set_image(self, image: Image) -> None: ...
    def show(self) -> None: ...
