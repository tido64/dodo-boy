# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Tests for the trip module that fetches data from Entur.
"""

import os
from typing import List

from dodotypes import Trip
from trip_entur_org import parse_trips


def test_parse_trips() -> None:
    """parse_trips() returns trips to display"""
    source_dir: str = os.path.dirname(__file__)
    test_data: str = os.path.join(source_dir, "trip_entur_org_test.json")
    with open(test_data, encoding="utf-8") as response:
        trips: List[Trip] = parse_trips(response.read())

    assert len(trips) == 2

    assert trips[0].start_time == "2021-02-05T14:03:00+0100"
    assert trips[0].mode == "bus"
    assert trips[0].name == "Oslo bussterminal"
    assert trips[0].line_code == "300"

    assert trips[1].start_time == "2021-02-06T14:03:00+0100"
    assert trips[1].mode == "bus"
    assert trips[1].name == "Oslo bussterminal"
    assert trips[1].line_code == "300"
