# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Tests for the weather module that fetches data from Meteorologisk Institutt.
"""

import os

from dodotypes import Forecast
from weather_met_no import get_current_data


def test_get_current_data() -> None:
    """get_current_data() returns air temperature and weather symbol to display"""
    source_dir: str = os.path.dirname(__file__)
    test_data: str = os.path.join(source_dir, "weather_met_no_test.json")
    with open(test_data, "r") as response:
        forecast: Forecast = get_current_data(response.read())
    assert forecast.air_temperature == -12.3
    assert forecast.symbol == "partlycloudy_night"
