import pickle
from dataclasses import asdict
from datetime import datetime as dt

import pytest
import pytz

from musync.entity import Origin, Track
from tests.unittests.entity import DATA_DIR


@pytest.fixture
def spotify_track():
    with open(DATA_DIR / "test_track_spotify.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def tidal_track():
    with open(DATA_DIR / "test_track_tidal.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def loaded_spotify_track(spotify_track):
    return Track.from_spotify(spotify_track)


@pytest.fixture
def loaded_tidal_track(tidal_track):
    return Track.from_tidal(tidal_track)


def test_track_from_spotify(spotify_track):
    track = Track.from_spotify(spotify_track)

    assert track.track_id == "2yTFrY6qG6l46rfVtQDVim"
    assert track.artist_ids == ["7G1GBhoKtEPnP86X2PvEYO", "586uxXMyD5ObPuzjtrzO1Q"]
    assert track.name == "Sinnerman - Sofi Tukker Remix"
    assert track.date_added == dt(2024, 2, 10, 14, 17, 45).replace(
        tzinfo=pytz.utc
    )  # 2024-02-10T14:17:45Z
    assert track.origin == Origin.SPOTIFY


def test_track_from_tidal(tidal_track):
    track = Track.from_tidal(tidal_track)

    assert track.track_id == "123456789"
    assert track.artist_ids == ["18272666"]
    assert track.name == "Ovni"
    assert track.date_added == dt(2023, 12, 29, 16, 0, 34).replace(
        tzinfo=pytz.utc
    )  # 2023-12-29 16:00:34.856000+00:00
    assert track.origin == Origin.TIDAL


def test_equals_with_different_tracks(loaded_tidal_track, loaded_spotify_track):
    assert not loaded_tidal_track.equals(loaded_spotify_track)
    assert not loaded_spotify_track.equals(loaded_tidal_track)


def test_equals_with_invalid_type(loaded_spotify_track, loaded_tidal_track):
    with pytest.raises(TypeError):
        loaded_spotify_track.equals("invalid")

    with pytest.raises(TypeError):
        loaded_tidal_track.equals("invalid")


def test_equals_with_identical_tracks(loaded_spotify_track, loaded_tidal_track):
    assert loaded_spotify_track.equals(loaded_spotify_track)
    assert loaded_tidal_track.equals(loaded_tidal_track)


def test_equals_with_same_track_from_different_platform(loaded_tidal_track):
    track_dict = asdict(loaded_tidal_track)
    track_dict["origin"] = Origin.UNKNOWN
    other_track = Track(**track_dict)
    assert loaded_tidal_track.equals(other_track)
