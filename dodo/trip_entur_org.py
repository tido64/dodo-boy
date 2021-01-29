# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Trip module that fetches data from Entur.

Documentation: https://developer.entur.org/pages-journeyplanner-journeyplanner-v2
"""

import json
from typing import Any, Dict, List
import urllib.parse
import urllib.request

from dodotypes import Coordinates, Destination, Trip

HEADERS = {
    "Content-Type": "application/json",
    "ET-Client-Name": "awesomecompany-awesomeapp",
}

JOURNEY_PLANNER = "https://api.entur.io/journey-planner/v2/graphql"

QUERY = """{{
  trip(
    from: {{
      coordinates: {{
        latitude: {lat}
        longitude: {lon}
      }}
    }}
    to: {{
      place: "{place}"
      name: "{name}"
    }}
    numTripPatterns: {count}
    maximumTransfers: 0
  )
  {{
    tripPatterns {{
      legs {{
        aimedStartTime
        mode
        toPlace {{
          name
        }}
        line {{
          id
          name
          publicCode
        }}
      }}
    }}
  }}
}}
"""


def _trip(leg: Dict[str, Any]) -> Trip:
    return Trip(
        start_time=leg["aimedStartTime"],
        mode=leg["mode"],
        name=leg["toPlace"]["name"],
        line_code=leg["line"]["publicCode"],
    )


def _parse_trip(trips: List[Trip], pattern: Dict[str, Any]) -> List[Trip]:
    leg = next((_trip(leg) for leg in pattern["legs"] if leg["line"] is not None), None)
    if leg is not None:
        trips.append(leg)
    return trips


def parse_trips(response: str) -> List[Trip]:
    """Parses trips returned by Journey Planner.

    :param response: JSON response returned by Journey Planner
    :type response: str
    :returns: Next departures
    :rtype: List[Trip]
    """
    trips: List[Trip] = []
    patterns: List[Dict[str, Any]] = json.loads(response)["data"]["trip"][
        "tripPatterns"
    ]

    # Custom 'reduce' implementation because of a typing bug.
    for pattern in patterns:
        trips = _parse_trip(trips, pattern)

    return sorted(trips, key=lambda trip: trip.start_time)


def get_next_departures(home: Coordinates, dest: Destination, count: int) -> List[Trip]:
    """Get the next departures for specified trip.

    :param home: Starting coordinates in decimal degrees
    :type home: Coordinates
    :param dest: Target destination
    :type dest: Destination
    :param count: Number of trips to fetch
    :type count: int
    :returns: Next departures
    :rtype: List[Trip]
    """
    body = json.dumps(
        {
            "query": QUERY.format(
                lat=home.lat,
                lon=home.lon,
                place=dest.place,
                name=dest.name,
                count=count,
            )
        }
    )
    request = urllib.request.Request(
        JOURNEY_PLANNER, body.encode("ascii"), headers=HEADERS
    )
    with urllib.request.urlopen(request) as response:
        return parse_trips(response.read())
