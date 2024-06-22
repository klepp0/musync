import pickle
from pathlib import Path

import pytest

from musync.entity import User

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def tidal_user():
    with open(DATA_DIR / "test_user_tidal.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def spotify_user():
    with open(DATA_DIR / "test_user_spotify.pkl", "rb") as f:
        return pickle.load(f)


def test_user_from_spotify(spotify_user):
    user = User.from_spotify(spotify_user)

    assert user.user_id == "9876543210"
    assert user.name == "Jane Doe"


def test_user_from_tidal(tidal_user):
    user = User.from_tidal(tidal_user)

    assert user.user_id == "123456789"
    assert user.name == "jane.doe"
