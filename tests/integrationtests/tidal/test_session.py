import pytest

from musync.entity import Playlist, User
from musync.tidal import TidalSession
from tests.unittests.entity import DATA_DIR


@pytest.fixture
def tidal_session():
    return TidalSession()


def test_session_is_logged_in(tidal_session):
    assert tidal_session.check_login()


def test_session_user(tidal_session):
    assert isinstance(tidal_session.user, User)


def test_session_get_playlists(tidal_session):
    assert all(isinstance(p, Playlist) for p in tidal_session.get_playlists())
