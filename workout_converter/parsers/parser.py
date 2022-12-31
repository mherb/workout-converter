from .wahoo import WahooParser
from .zwift import ZwiftParser

class Parser(object):
    
    PARSERS = [
        WahooParser,
        ZwiftParser
    ]
    
    @staticmethod
    def get_by_format(format: str):
        for parser_cls in Parser.PARSERS:
            if parser_cls.FORMAT == format:
                return parser_cls
        return None

    @staticmethod
    def get_by_file_ext(file_ext: str):
        for parser_cls in Parser.PARSERS:
            if parser_cls.FILE_EXT == file_ext:
                return parser_cls
        return None

    @staticmethod
    def gen_filename(name: str) -> str:
        return name.replace(": ", "_").replace("/", "-").replace("%", "P").replace("#", "").replace(" ", "_")
