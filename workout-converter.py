import argparse
import os
from pathlib import Path
from workout_converter.parsers import ZwiftParser
from workout_converter.parsers import WahooParser


def gen_filename(name: str) -> str:
    return name.replace(": ", "_").replace("/", "-").replace("%", "P").replace("#", "").replace(" ", "_")


def main(args):
    workout = ZwiftParser(args.input).load()

    if len(args.category) > 0 and len(workout.category) == 0:
        workout.category = args.category
    if len(args.subcategory) > 0 and len(workout.subcategory) == 0:
        workout.subcategory = args.subcategory

    out_folder = Path(args.output_dir)
    os.makedirs(out_folder, exist_ok=True)
    filename = "{}.{}".format(gen_filename(workout.full_name), WahooParser.FILE_EXT)
    WahooParser(out_folder / filename).save(workout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert Zwift Workout file to Wahoo Workout Plan")

    parser.add_argument("input", type=str)
    parser.add_argument("output_dir", type=str)
    parser.add_argument("--name-prefix", type=str, default="")
    parser.add_argument("--category", type=str, default="")
    parser.add_argument("--subcategory", type=str, default="")
    args = parser.parse_args()

    main(args)
