"""Game assets and where they are located. This is a lazy/OK solution 
to creating a singleton class."""

# This is kind of like a singleton class. It isn't a class though. It is a module.
# See discussion at
# https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python
# More information about the singleton design pattern is available on Wikipedia,
# https://en.wikipedia.org/wiki/Singleton_pattern.

from os import path
from .galaga_asset_dict import galaga_asset_dict as asset_dict

# The absolute path of the current file's directory.
main_dir = path.split(path.abspath(__file__))[0]
# We'll join "data" to our main_dir and that's where we will store our game assets.
# Not the best location but it is good enough for our needs in CPSC 386.
data_dir = path.join(main_dir, "data")

# Dictionary of game assets. It's up to the programmer to keep track of all these
# different names. One may want to use a naming convention such as
# title:soundtrack, leve1:soundtrack, title:splash, level1:player,
# level1:npc1, level1:npc2, etc.
# asset_dict = {
#     'soundtrack': '8bp051-06-random-happy_ending_after_all.mp3',
# }
# Look up; the dictionary is defined in a file named movedemo_asset_dict.py and
# imported into this file as asset_dict.


def get(key):
    """Given the key representing the asset, return a fully qualified
    path to the asset."""
    # Throws a KeyError if key doesn't exist.
    try:
        value = asset_dict[key]
    except KeyError:
        print(
            f'The asset key {key} is unknown and a KeyError exception was raised.'
        )
        raise
    value = path.join(data_dir, value)
    # Make sure the path exists
    assert path.exists(value)
    return value
