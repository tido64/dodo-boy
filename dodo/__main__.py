# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""This is the main script (obviously).
"""

from functools import reduce
from operator import iconcat
from typing import List

from PIL import Image, ImageDraw, ImageFont
from config import get_config
from display import Display
from dodotypes import Trip
from font_roboto import Roboto  # pylint: disable=no-name-in-module
from time_utils import local_time, relative_time
from trip_entur_org import get_next_departures
from weather_met_no import get_forecast

config = get_config()

forecast = get_forecast(config.home)
trips: List[Trip] = reduce(
    iconcat,
    map(
        lambda t: get_next_departures(config.home, t.destination, t.entries),
        config.trips,
    ),
    [],
)
current_time = local_time(config.date_format, locale=config.locale)


def _format_trip(trip: Trip) -> str:
    """
    icons = {
        "air": "✈️",
        "bus": "🚌",
        "cableway": "🚠",
        "coach": "🚌",
        "funicular": "🚞",
        "lift": "🛗",
        "metro": "🚇",
        "rail": "🚋",
        "tram": "🚋",
        "unknown": "",
        "water": "🌊",
    }
    """
    time = relative_time(trip.start_time, locale=config.locale)
    return f"{trip.name.split()[0]}: {trip.line_code} {time}"


temperature = (
    round(forecast.air_temperature)
    if forecast.air_temperature != float("inf")
    else "--"
)
output = "\n".join(  # pylint: disable=invalid-name
    (
        f"{temperature}°C | {current_time}",
        *map(_format_trip, trips),
    )
)
print(output)

display = Display(config.inky)

image = Image.new(  # pylint: disable=invalid-name
    display.image_mode(), display.size(), display.WHITE
)
draw = ImageDraw.Draw(image)  # pylint: disable=invalid-name
font = ImageFont.truetype(Roboto, 16)  # pylint: disable=invalid-name
draw.multiline_text((4, 4), output, display.BLACK, font)

display.present(image)
