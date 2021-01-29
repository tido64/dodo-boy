# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Module for managing the Inky pHAT e-ink display.
"""

from typing import Tuple

from PIL import Image
from dodotypes import Config

try:
    from inky import InkyPHAT  # pylint: disable=no-name-in-module
except ImportError:
    pass


class Display:
    """Inky pHAT e-Ink Display"""

    WIDTH = 212
    HEIGHT = 104

    WHITE = 0
    BLACK = 1
    RED = 2
    YELLOW = 2

    def __init__(self, config: Config.Inky):
        try:
            self.inky_display = InkyPHAT(config.colour)
            self.inky_display.set_border(self.inky_display.WHITE)
        except NameError:
            self.WHITE = 255  # pylint: disable=invalid-name
            self.BLACK = 0  # pylint: disable=invalid-name

    def present(self, image: Image) -> None:
        """Presents specified image."""
        try:
            self.inky_display.set_image(image)
            self.inky_display.show()
        except AttributeError:
            image.show()

    def size(self) -> Tuple[int, int]:
        """Returns size of display."""
        try:
            return (self.inky_display.WIDTH, self.inky_display.HEIGHT)
        except AttributeError:
            return (self.WIDTH, self.HEIGHT)
