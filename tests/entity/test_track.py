import pickle
from pathlib import Path

import pytest

from musync.entity import Track

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def spotify_track():
    with open(DATA_DIR / "test_track_spotify.pkl", "rb") as f:
        return pickle.load(f)


def test_track_from_spotify(spotify_track):
    print(spotify_track)
    track = Track.from_spotify(spotify_track)

    assert track.track_id == "2yTFrY6qG6l46rfVtQDVim"
    assert track.artist_id == "7G1GBhoKtEPnP86X2PvEYO"
    assert track.name == "Sinnerman - Sofi Tukker Remix"
    assert track.date_added == "2024-02-10T14:17:45Z"

