import pytest

from musync.entity import Playlist, User
from musync.spotify.session import SpotifySession


@pytest.fixture
def spotify_session():
    return SpotifySession()


def test_session_is_logged_in(spotify_session):
    return spotify_session.check_login()


def test_session_user(spotify_session):
    assert isinstance(spotify_session.user, User)


def test_session_playlists(spotify_session):
    assert all(isinstance(p, Playlist) for p in spotify_session.get_playlists())
