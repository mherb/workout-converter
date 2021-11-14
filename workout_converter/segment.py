
from typing import List, Optional, Union
from enum import Enum


class TargetType(Enum):
    FTP_RELATIVE = "ftp_relative"
    POWER = "power"
    CADENCE = "cadence"
    HEARTRATE = "heartrate"


class SegmentType(Enum):
    WARMUP = "warmup"
    COOLDOWN = "cooldown"
    INTERVAL = "interval"
    STEADY = "steadystate"
    FREERIDE = "freeride"
    RAMP = "ramp"


class Target(object):
    ValueType = Optional[Union[int, float]]

    def __init__(self, type: TargetType,
                       value: ValueType = None,
                       high: ValueType = None,
                       low: ValueType = None,
                       start: ValueType = None,
                       end: ValueType = None):
        self.type = type
        self.value = self._parse_value(value)
        self.high = self._parse_value(high)
        self.low = self._parse_value(low)
        self.start = self._parse_value(start)
        self.end = self._parse_value(end)

    def _parse_value(self, value: ValueType) -> Optional[int]:
        if value is None:
            return None
        if type(value) is float and self.type == TargetType.FTP_RELATIVE:
            return int(100 * value)
        return int(value)

    def __call__(self, time: float) -> int:
        assert 0 <= time <= 1
        # Compute target value at relative point in time
        # time should be in [0, 1]
        if self.is_ramp():
            return int(self.start + time * (self.end - self.start))
        else:
            return self.value

    def is_ramp(self) -> bool:
        return self.start is not None and self.end is not None

    def is_range(self) -> bool:
        return self.low is not None and self.high is not None

    def is_valid(self) -> bool:
        return self.value is not None or self.is_range() or self.is_ramp()


class TargetSet(object):
    def __init__(self, targets: List[Target]):
        self.targets = {}
        for target in targets:
            if target.is_valid():
                self.targets[target.type] = target

    def __iter__(self):
        return iter(self.targets)

    def __getitem__(self, item):
        return self.targets[item]

    def __contains__(self, item):
        return item in self.targets

    def __getattr__(self, item):
        key = TargetType(item)
        if key in self.targets:
            return self.targets[key]
        else:
            return None


class SegmentEntry(object):
    def __init__(self, duration: int, targets: TargetSet, name: str = ""):
        self.duration = duration
        self.name = name
        self.targets = targets

    def is_ramp(self) -> bool:
        return any([target.is_ramp() for target in self.targets])


class Segment(object):
    def __init__(self, type: SegmentType, entries: List[SegmentEntry], name: str = "", repeat: int = 1):
        self.type = type
        self.name = name
        self.entries = entries
        self.repeat = repeat

    @property
    def description(self) -> str:
        if len(self.name) > 0:
            return self.name
        return self.type.value.upper()

    @property
    def duration(self) -> int:
        return self.repeat * sum([entry.duration for entry in self.entries])
