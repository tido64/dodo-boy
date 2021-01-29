# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Types"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Coordinates:
    """Coordinates"""

    lat: float
    lon: float


@dataclass(frozen=True)
class Destination:
    """Trip destination"""

    place: str
    name: str


@dataclass(frozen=True)
class Forecast:
    """Weather forecast"""

    air_temperature: float
    symbol: str


@dataclass(frozen=True)
class Trip:
    """Planned trip"""

    start_time: str
    mode: str
    name: str
    line_code: str


@dataclass(frozen=True)
class Config:
    """User configuration"""

    @dataclass(frozen=True)
    class Inky:
        """Inky display configuration"""

        type: str
        colour: str

    @dataclass(frozen=True)
    class Trip:
        """Trip configuration"""

        destination: Destination
        entries: int

    locale: str
    date_format: str
    home: Coordinates
    trips: List[Trip]
    inky: Inky
