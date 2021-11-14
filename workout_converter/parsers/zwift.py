from pathlib import Path
from ..workout import Workout
from ..segment import Segment, SegmentEntry, SegmentType, Target, TargetSet, TargetType
import xml.etree.ElementTree as ET


class ZwiftParser(object):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    def load(self) -> Workout:
        try:
            root = ET.parse(self._file_path).getroot()
            return self._parse_workout(root)
        except ET.ParseError as e:
            print("Error parsing {}".format(self._file_path))
            raise e

    def _parse_workout(self, root: ET.Element) -> Workout:
        name = root.findtext("name")
        description = root.findtext("description")
        author = root.findtext("author")
        category = root.findtext("category")
        subcategory = root.findtext("subcategory")

        segments = [self._parse_segment(s) for s in root.find("workout")]

        return Workout(name=name, description=description,
                       author=author, category=category, subcategory=subcategory,
                       segments=segments)

    def _parse_segment(self, segment: ET.Element) -> Segment:
        tag = segment.tag.lower()
        attr = lambda name, default=None, dtype=int: \
            dtype(segment.attrib[name]) if name in segment.attrib else default
        if tag == "intervalst":
            on_ftp = Target(TargetType.FTP_RELATIVE,
                            value=attr("OnPower", dtype=float),
                            high=attr("PowerOnHigh", dtype=float),
                            low=attr("PowerOnLow", dtype=float))
            on_cad = Target(TargetType.CADENCE,
                            value=attr("Cadence"),
                            high=attr("CadenceHigh"),
                            low=attr("CadenceLow"))
            on = SegmentEntry(duration=attr("OnDuration"),
                              targets=TargetSet([on_ftp, on_cad]))

            off_ftp = Target(TargetType.FTP_RELATIVE,
                             value=attr("OffPower", dtype=float),
                             high=attr("PowerOffHigh", dtype=float),
                             low=attr("PowerOffLow", dtype=float))
            off_cad = Target(TargetType.CADENCE,
                             value=attr("CadenceResting"))
            off = SegmentEntry(duration=attr("OffDuration"),
                               targets=TargetSet([off_ftp, off_cad]))
            return Segment(type=SegmentType.INTERVAL, entries=[on, off],
                           repeat=attr("Repeat", 1))
        else:
            if tag in ["ramp", "warmup", "cooldown"]:
                ftp = Target(TargetType.FTP_RELATIVE,
                             value=attr("Power", dtype=float),
                             start=attr("PowerLow", dtype=float),
                             end=attr("PowerHigh", dtype=float))
            else:
                ftp = Target(TargetType.FTP_RELATIVE,
                             value=attr("Power", dtype=float),
                             high=attr("PowerHigh", dtype=float),
                             low=attr("PowerLow", dtype=float))
            cad = Target(TargetType.CADENCE,
                            value=attr("Cadence"),
                            high=attr("CadenceHigh"),
                            low=attr("CadenceLow"))
            entry = SegmentEntry(duration=attr("Duration"),
                                 targets=TargetSet([ftp, cad]))

            return Segment(type=self._get_type_from_tag(tag), entries=[entry])

    def _get_type_from_tag(self, tag) -> SegmentType:
        if tag == "warmup":
            return SegmentType.WARMUP
        elif tag == "cooldown":
            return SegmentType.COOLDOWN
        elif tag == "intervalst":
            return SegmentType.INTERVAL
        elif tag == "ramp":
            return SegmentType.RAMP
        elif tag == "steadystate":
            return SegmentType.STEADY
        elif tag == "freeride":
            return SegmentType.FREERIDE
        return None

    def save(self, workout: Workout):
        raise NotImplementedError()
