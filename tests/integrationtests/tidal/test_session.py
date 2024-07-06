import datetime
import pickle

import pytest

# from musync.common.entity import Origin, Playlist, Track, User
from musync.app.models import Origin, Playlist, Track, User
from musync.tidal import TidalSession
from tests.unittests.common.entity import DATA_DIR


@pytest.fixture
def tidal_session():
    return TidalSession()


@pytest.fixture
def spotify_track():
    with open(DATA_DIR / "test_track_spotify.pkl", "rb") as f:
        return Track.from_spotify(pickle.load(f))


@pytest.fixture
def tidal_track():
    with open(DATA_DIR / "test_track_tidal.pkl", "rb") as f:
        return Track.from_tidal(pickle.load(f))


@pytest.fixture
def tidal_track_list():
    tracks = [
        Track(
            track_id="338383176",
            artist_ids=["7343085"],
            name="Cabalero",
            duration=datetime.timedelta(seconds=345),
            origin=Origin.TIDAL,
        ),
        Track(
            track_id="304574491",
            artist_ids=["10644748", "6576000"],
            name="Tension",
            duration=datetime.timedelta(seconds=263),
            origin=Origin.TIDAL,
        ),
        Track(
            track_id="121277192",
            artist_ids=["15910495"],
            name="Overdub (Original Mix)",
            duration=datetime.timedelta(seconds=348),
            origin=Origin.TIDAL,
        ),
    ]
    return tracks


@pytest.fixture
def create_playlist(tidal_session):
    title = "Test Playlist"
    description = (
        "This playlist was created by the https://github.com/klepp0/musync project."
    )
    tidal_response = tidal_session._client.user.create_playlist(title, description)
    new_playlist = Playlist.from_tidal(tidal_response)

    yield new_playlist

    tidal_session._client.playlist(new_playlist.playlist_id).delete()


def test_session_is_logged_in(tidal_session):
    assert tidal_session.check_login()


def test_session_user(tidal_session):
    assert isinstance(tidal_session.user, User)


def test_session_load_not_existing_playlist(tidal_session):
    assert tidal_session.load_playlist("foo") is None


def test_session_load_existing_playlist(tidal_session):
    tidal_playlist = tidal_session.load_playlist("281820fd-30e6-4240-9356-e07244a37bc8")
    assert isinstance(tidal_playlist, Playlist)


def test_session_load_playlists(tidal_session):
    assert all(isinstance(p, Playlist) for p in tidal_session.load_playlists())


def test_search_track(tidal_session, spotify_track):
    tidal_track = tidal_session.find_track(spotify_track)
    assert spotify_track.equals(tidal_track)


def test_add_to_playlist(tidal_session, create_playlist, tidal_track_list):
    playlist = create_playlist
    n_tracks_before = playlist.n_tracks
    updated_playlist = tidal_session.add_to_playlist(playlist, tidal_track_list)
    n_tracks_after = updated_playlist.n_tracks

    assert playlist.playlist_id == updated_playlist.playlist_id
    assert n_tracks_before < n_tracks_after
