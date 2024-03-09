# pygcode

GCODE Parser for Python

Currently in development, `pygcode` is a low-level GCode interpreter
for python.


# Installation

Somthing in the order of
```
    git clone git@github.com:petaflot/pygcode.git --depth=1
    cd pygcode
    pip install -e .
```

## Configuration

Make sure you set `_DEFAULT_` to the dialect you want to use in `src/pygcode/dialects/__init__.py` ; this is absolutely suboptimal, contributions are welcome. Also, note that `marlin2` flavor covers all versions of Marlin ; due to some functional redundances, some commands have been commented out (typically for bed leveling and delta bots, see `src/pygcode/gcodes_marlin.py`).


# Documentation

[Check out the wiki](https://github.com/fragmuffin/pygcode/wiki) for documentation.
