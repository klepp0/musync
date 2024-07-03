import pickle

import pytest

from musync.entity import Playlist, Track, User
from musync.spotify import SpotifySession
from tests.unittests.entity import DATA_DIR


@pytest.fixture
def spotify_session():
    return SpotifySession()


@pytest.fixture
def tidal_track():
    with open(DATA_DIR / "test_track_tidal.pkl", "rb") as f:
        return Track.from_tidal(pickle.load(f))


def test_session_is_logged_in(spotify_session):
    return spotify_session.check_login()


def test_session_user(spotify_session):
    assert isinstance(spotify_session.user, User)


def test_session_playlists(spotify_session):
    assert all(isinstance(p, Playlist) for p in spotify_session.get_playlists())


def test_find_track(spotify_session, tidal_track):
    spotify_track = spotify_session.find_track(tidal_track)
    assert tidal_track.equals(spotify_track)
