import argparse
import os
from pathlib import Path
from workout_converter.parsers import Parser


def convert(args):
    input_path = Path(args.input)

    file_ext = input_path.suffix[1:]
    source_cls = Parser.get_by_file_ext(file_ext)

    if source_cls is None:
        print("ERROR: Unknown input parser for file ext: {}".format(file_ext))
        exit(-1)
    
    target_cls = Parser.get_by_format(args.format)
    if target_cls is None:
        print("ERROR: Unknown target format parser: {}".format(args.format))
        exit(-2)
    
    print("Converting {} to {}...".format(source_cls.NAME, target_cls.NAME))
    
    try:
        workout = source_cls(input_path).load()
    except NotImplementedError:
        print("ERROR: Reading not implemented for parser '{}'".format(source_cls.NAME))
        exit(-1)

    # Override category and subcategory
    if len(args.category) > 0 and len(workout.category) == 0:
        workout.category = args.category
    if len(args.subcategory) > 0 and len(workout.subcategory) == 0:
        workout.subcategory = args.subcategory

    # Save
    output_path = input_path.parent if args.output is None or len(args.output) == 0 else Path(args.output)
    if output_path.is_dir():
        filename = input_path.stem if not args.filename_title else Parser.gen_filename(workout.full_name)
        output_path = output_path / "{}.{}".format(filename, target_cls.FILE_EXT)
        
    try:
        target_cls(output_path).save(workout)
    except NotImplementedError:
        print("ERROR: Writing not implemented for parser '{}'".format(target_cls.NAME))


def list_formats():
    print("Available formats:")
    for parser_cls in Parser.PARSERS:
        print("  {}: {} (.{})".format(parser_cls.FORMAT, parser_cls.NAME, parser_cls.FILE_EXT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Workout File Converter")

    parser.add_argument("input", type=str, nargs='?', default="", help="Input workout file")
    parser.add_argument("-o", "--output", type=str, help="Output directory or file where converted file is saved")
    parser.add_argument("-f", "--format", type=str, help="Output format (use -F for available formats)")
    parser.add_argument("-F", "--formats", action='store_true', help="List available formats and parsers")
    parser.add_argument("--category", type=str, default="", help="Workout category metadata")
    parser.add_argument("--subcategory", type=str, default="", help="Workout subcategory metadata")
    parser.add_argument("--filename_title", action='store_true', help="Use workout title as filename")
    
    args = parser.parse_args()

    if args.formats:
        list_formats()
    else:
        if args.input is None or len(args.input) == 0:
            parser.error("input file is required")
        if args.format is None or len(args.format) == 0:
            parser.error("target format (-f, --format) is required")
        convert(args)

