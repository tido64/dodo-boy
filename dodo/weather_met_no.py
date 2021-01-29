# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Weather module that fetches data from Meteorologisk Institutt.

Documentation: https://api.met.no/
"""

import json
from typing import Any, Dict
from urllib.error import HTTPError
import urllib.parse
import urllib.request

from dodotypes import Coordinates, Forecast

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "curl/7.64.1",
}

# Locationforecast 2.0
# https://api.met.no/weatherapi/locationforecast/2.0/documentation#!/data/get_compact
LOCATION_FORECAST = "https://api.met.no/weatherapi/locationforecast/2.0/compact"


def get_current_data(response: str) -> Forecast:
    """Parses the JSON string returned by Locationforecast 2.0.

    :param response: JSON response returned by Locationforecast 2.0
    :type response: str
    :returns: An object with the air temperature and weather symbol to display
    :rtype: Forecast
    """
    data: Dict[str, Any] = json.loads(response)
    data = data["properties"]["timeseries"][0]["data"]
    return Forecast(
        air_temperature=data["instant"]["details"]["air_temperature"],
        symbol=data["next_1_hours"]["summary"]["symbol_code"],
    )


def get_forecast(home: Coordinates) -> Forecast:
    """Retrieves the forecast at specified location.

    :param home: Coordinates in decimal degrees
    :type home: Coordinates
    :returns: An object with the air temperature and weather symbol to display
    :rtype: Forecast
    """
    params = urllib.parse.urlencode(
        {
            "lat": str(home.lat),
            "lon": str(home.lon),
        }
    )
    request = urllib.request.Request(LOCATION_FORECAST + "?" + params, headers=HEADERS)
    try:
        with urllib.request.urlopen(request) as response:
            return get_current_data(response.read())
    except HTTPError:
        return Forecast(air_temperature=float("inf"), symbol="")
