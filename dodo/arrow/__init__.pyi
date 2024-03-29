# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring, unused-argument, undefined-variable
from datetime import datetime
from typing import Any, List, Union

class Arrow:
    def format(self, fmt: str = ..., locale: str = ...) -> str: ...
    def humanize(
        self,
        other: Union[Arrow, datetime, None] = ...,
        locale: str = ...,
        only_distance: bool = ...,
        granularity: Union[str, List[str]] = ...,
    ) -> str: ...

def get(*args: Any, **kwargs: Any) -> Arrow: ...
def utcnow() -> Arrow: ...
def now(tz: str = ...) -> Arrow: ...
