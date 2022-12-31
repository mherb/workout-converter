import abc
from pathlib import Path

from ..workout import Workout

class ParserBase(abc.ABC):
    def __init__(self, file_path: Path):
        super().__init__()
        self._file_path = file_path

    @property
    def name(self) -> str:
        self.NAME

    @property
    def format(self) -> str:
        self.FORMAT

    @property
    def file_ext(self) -> str:
        self.FILE_EXT

    @abc.abstractmethod
    def load(self) -> Workout:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, workout: Workout):
        raise NotImplementedError()
