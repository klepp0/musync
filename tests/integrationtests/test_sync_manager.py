import pytest

from musync.common.sync_manager import SyncManager
from musync.common.entity import Playlist, Track
from musync.spotify import SpotifySession
from musync.tidal import TidalSession


@pytest.fixture
def sync_manager():
    session1 = SpotifySession()
    session2 = TidalSession()
    return SyncManager(session1, session2)


def test_get_common_playlists(sync_manager):
    playlists = sync_manager.get_common_playlists()
    assert all(
        isinstance(p1, Playlist) and isinstance(p2, Playlist) for p1, p2 in playlists
    )
    assert all(p1.name == p2.name for p1, p2 in playlists)


def test_get_missing_tracks(sync_manager):
    p1, p2 = sync_manager.get_common_playlists()[0]
    missing_tracks = sync_manager.get_missing_tracks(p1, p2)

    assert all(isinstance(track, Track) for track in missing_tracks)
