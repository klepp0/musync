import pickle
from pathlib import Path

import pytest

from musync.entity import Playlist

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def spotify_playlist():
    with open(DATA_DIR / "test_playlist_spotify.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def tidal_playlist():
    with open(DATA_DIR / "test_playlist_tidal.pkl", "rb") as f:
        return pickle.load(f)


def test_playlist_from_spotify(spotify_playlist):
    playlist = Playlist.from_spotify(spotify_playlist)

    assert playlist.playlist_id == "mockPlaylistId"
    assert playlist.owner_id == "mockUserId"
    assert playlist.name == "Mock Playlist 🎶"
    assert playlist.n_tracks == 10


def test_playlist_from_tidal(tidal_playlist):
    playlist = Playlist.from_tidal(tidal_playlist)

    assert playlist.playlist_id == "123456789"
    assert playlist.owner_id == "123456789"
    assert playlist.name == "✨ Mock Playlist"
    assert playlist.n_tracks == 36
