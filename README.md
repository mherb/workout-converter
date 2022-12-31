# Workout Converter

This is a tiny command line tool to convert between different file formats for structured workouts (mostly cycling-based for usage on smart-trainers).

## Usage

Please clean the repo to get the source code

    git clone https://github.com/mherb/workout-converter.git && cd workout-converter

You can convert a workout file that you have created or downloaded using

    python3 workout-converter.py -f <targetformat> <input file>

which will be saved with the same name (but different extension) in the same path as the input file.
Please have a look at the command line help (`-h`) for additional options.

You can query the list of available output formats:

    python3 workout-converter.py -F

## File Formats

At the moment, the following file formats are supported for reading/writing

| Format        | Read               | Write              | Comment                    |
|---------------|--------------------|--------------------|----------------------------|
| Wahoo (.plan) | :x:                | :white_check_mark: | for Wahoo ELEMNT headunits |
| Zwift (.zwo)  | :white_check_mark: | :x:                |                            |

Additional support can be easily added by implmenting a corresponding [parser](workout_converter/parsers)

## References

Below are some helpful resources and related projects about various workout file formats

- [Intyre/wahoo_elemnt](https://gist.github.com/Intyre/2c0a8e337671ed6f523950ef08e3ca3f)
- [h4l/zwift-workout-file-reference](https://github.com/h4l/zwift-workout-file-reference)
- [ManuelWiese/mrc_tools](https://github.com/ManuelWiese/mrc_tools)
- [mhanney/zwoparse](https://github.com/mhanney/zwoparse)
