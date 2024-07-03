import pickle

import pytest

from musync.entity import Playlist, Track, User
from musync.tidal import TidalSession
from tests.unittests.entity import DATA_DIR


@pytest.fixture
def tidal_session():
    return TidalSession()


@pytest.fixture
def spotify_track():
    with open(DATA_DIR / "test_track_spotify.pkl", "rb") as f:
        return Track.from_spotify(pickle.load(f))


def test_session_is_logged_in(tidal_session):
    assert tidal_session.check_login()


def test_session_user(tidal_session):
    assert isinstance(tidal_session.user, User)


def test_session_load_playlists(tidal_session):
    assert all(isinstance(p, Playlist) for p in tidal_session.load_playlists())


def test_search_track(tidal_session, spotify_track):
    tidal_track = tidal_session.find_track(spotify_track)
    assert spotify_track.equals(tidal_track)
