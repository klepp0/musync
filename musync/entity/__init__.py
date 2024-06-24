from enum import IntEnum

from .artist import Artist
from .playlist import Playlist
from .track import Track
from .user import User


class Origin(IntEnum):
    unknown = 0
    spotify = 1
    tidal = 2
