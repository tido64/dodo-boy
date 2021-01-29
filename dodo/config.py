# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Config
"""

import argparse
import json
import sys
from typing import Any, Dict

from dodotypes import Config, Coordinates, Destination


def _make_trip(trip: Dict[str, Any]) -> Config.Trip:
    return Config.Trip(
        destination=Destination(
            place=trip["destination"]["place"],
            name=trip["destination"]["name"],
        ),
        entries=trip["entries"],
    )


def read_config(path: str) -> Config:
    """Reads configuration file at specified path.

    :param path: Path to the configuration file to read
    :type path: str
    :returns: Configuration object parsed from the configuration file
    :rtype: Config
    """
    with open(path, "r") as config_file:
        config: Dict[str, Any] = json.load(config_file)
    return Config(
        locale=config["locale"],
        date_format=config["dateFormat"],
        home=Coordinates(
            lat=config["home"]["lat"],
            lon=config["home"]["lon"],
        ),
        trips=list(map(_make_trip, config["trips"])),
        inky=Config.Inky(
            type=config["inky"]["type"],
            colour=config["inky"]["colour"],
        ),
    )


def get_config() -> Config:
    """Retrieves user configuration.

    :returns: User configuration object
    :rtype: Config
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, help="specify configuration file")
    args = parser.parse_args()

    try:
        return read_config("config.json" if args.config is None else args.config)
    except (FileNotFoundError, IsADirectoryError) as err:
        sys.exit(err)
    except TypeError:
        sys.exit("No configuration file was specified")
