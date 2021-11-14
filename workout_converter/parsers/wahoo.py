from pathlib import Path
import textwrap
from typing import List
from ..workout import Workout
from ..segment import Segment, SegmentEntry, SegmentType, Target, TargetSet, TargetType


class WahooParser(object):

    FILE_EXT = "plan"

    def __init__(self, file_path: Path):
        self._file_path = file_path

    def load(self) -> Workout:
        raise NotImplementedError()

    def save(self, workout: Workout):
        data = self._generate_plan(workout)
        with self._file_path.open(mode='w') as f:
            f.write("\n".join(data))

    def _generate_plan(self, workout: Workout) -> List[str]:
        data = self._generate_header(workout)
        for segment in workout.segments:
            data += self._generate_interval(segment)
        return data

    def _generate_header(self, workout: Workout) -> List[str]:
        data = []
        data.append("=HEADER=")
        data.append("NAME={}".format(workout.full_name))
        data.append("# Provider: {}".format(workout.author))
        data.append("DURATION={}".format(workout.duration))
        data.append("PLAN_TYPE=0")  # STRUCTURED_WORKOUT
        data.append("WORKOUT_TYPE=0")  # BIKE
        for line in textwrap.wrap(workout.description, 80):
            data.append("DESCRIPTION={}".format(line))
        data.append("")
        data.append("=STREAM=")

        return data

    def _generate_interval(self, segment: Segment) -> List[str]:
        data = ["=INTERVAL="]

        data.append("INTERVAL_NAME={}".format(segment.description))

        if len(segment.entries) > 1:
            # Exit interval immediately to first subinterval
            data.append("MESG_DURATION_SEC>=0?EXIT")

        if segment.repeat > 1:
            data.append("REPEAT={}".format(segment.repeat-1))

        for entry in segment.entries:
            if len(segment.entries) > 1:
                data.append("=SUBINTERVAL=")
            # TODO: subinterval name?
            for target in entry.targets:
                data += self._generate_interval_target(entry.targets[target], entry.duration)
            data.append("MESG_DURATION_SEC>={}?EXIT".format(entry.duration))
            data.append("")

        return data

    def _generate_interval_target(self, target: Target, duration: int) -> List[str]:
        prefix = ""
        if target.type == TargetType.FTP_RELATIVE:
            prefix = "PERCENT_FTP"
        elif target.type == TargetType.CADENCE:
            prefix = "CAD"
        elif target.type == TargetType.HEARTRATE:
            prefix = "HR"
        elif target.type == TargetType.POWER:
            prefix = "PWR"

        data = []

        low = target.low or target.value or target.start
        high = target.high or target.value or target.start

        if low is not None:
            data.append("{}_LO={}".format(prefix, low))
        if high is not None:
            data.append("{}_HI={}".format(prefix, high))

        if target.is_ramp():
           # Output special ramp sequence
           target_delta = target.end - target.start
           time_delta_per_target_delta = duration / target_delta
           time_step = max(10, int(time_delta_per_target_delta))

           time = 0
           while time <= duration:
               value = target(time / duration)
               data.append("MESG_DURATION_SEC>={}?{}_LO={}".format(time, prefix, value))
               data.append("MESG_DURATION_SEC>={}?{}_HI={}".format(time, prefix, value))
               time += time_step

        return data

