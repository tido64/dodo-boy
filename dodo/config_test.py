# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Config tests
"""

import os

from config import read_config


def test_read_config() -> None:
    """read_config() parses a config file"""
    source_dir: str = os.path.dirname(__file__)
    config = read_config(os.path.join(os.path.dirname(source_dir), "config.json"))
    assert config.locale == "nb_no"
    assert config.date_format == "ddd, D MMM HH:mm"
    assert config.home.lat == 59.90706253051758
    assert config.home.lon == 10.760673522949219
    assert config.trips[0].destination.place == "NSR:StopPlace:337"
    assert config.trips[0].destination.name == "Oslo S"
    assert config.trips[0].entries == 2
    assert config.trips[1].destination.place == "NSR:StopPlace:4489"
    assert config.trips[1].destination.name == "Lillestrøm bussterminal"
    assert config.trips[1].entries == 2
    assert config.inky.type == "phat"
    assert config.inky.colour == "black"
