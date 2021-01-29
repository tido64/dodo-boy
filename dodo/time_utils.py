# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

"""Time utilities
"""

import arrow


def local_time(fmt: str, locale: str) -> str:
    """Returns current timestamp in configured format and locale.

    :param fmt: Desired date/time format
    :type fmt: str
    :param locale: Desired locale
    :type locale: str
    :returns: Timestamp in configured format and locale
    :rtype: str
    """
    return arrow.now().format(fmt, locale=locale)


def relative_time(timestamp: str, locale: str) -> str:
    """Returns specified time as a human-readable relative time string.

    :param timestamp: Timestamp to make human-readable string for
    :type timestamp: str
    :returns: Relative time, e.g. "in 4 minutes"
    :rtype: str
    """
    time = arrow.get(timestamp).humanize(locale=locale)
    if locale == "nb_no":
        return time.replace("minutter", "min.").replace("sekunder", "sek.")
    return time
