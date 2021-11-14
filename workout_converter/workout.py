from typing import Optional, List
from .segment import Segment


class Workout(object):
    def __init__(self,
                 name: str,
                 description: str,
                 segments: List[Segment],
                 author: Optional[str] = None,
                 category: Optional[str] = None,
                 subcategory: Optional[str] = None
                 ):
        self.name = name.strip()
        self.description = (description or '').replace("\n", "").strip()
        self.author = author or ''
        self.category = category or ''
        self.subcategory = subcategory or ''
        self.segments = segments

    @property
    def full_name(self) -> str:
        name = ""
        if len(self.category) > 0:
            name += "{}: ".format(self.category)
        if len(self.subcategory) > 0:
            name += "{}/".format(self.subcategory)
        name += self.name
        return name

    @property
    def duration(self) -> int:
        return sum([segment.duration for segment in self.segments])
