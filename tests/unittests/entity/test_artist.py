import pickle

import pytest

from musync.entity import Artist, Origin
from tests.unittests.entity import DATA_DIR


@pytest.fixture
def spotify_artist():
    with open(DATA_DIR / "test_artist_spotify.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def tidal_artist():
    with open(DATA_DIR / "test_artist_tidal.pkl", "rb") as f:
        return pickle.load(f)


def test_artist_from_spotify(spotify_artist):
    artist = Artist.from_spotify(spotify_artist)

    assert artist.artist_id == "3jOstUTkEu2JkjvRdBA5Gu"
    assert artist.name == "Weezer"
    assert artist.origin == Origin.SPOTIFY


def test_artist_from_tidal(tidal_artist):
    artist = Artist.from_tidal(tidal_artist)

    assert artist.artist_id == "18272666"
    assert artist.name == "Vodoom"
    assert artist.origin == Origin.TIDAL
