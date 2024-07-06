import datetime
import pickle

import pytest

# from musync.common.entity import Origin, Playlist, Track, User
from musync.app.models import Origin, Playlist, Track, User
from musync.spotify import SpotifySession
from tests.unittests.common.entity import DATA_DIR


@pytest.fixture
def spotify_session():
    return SpotifySession()


@pytest.fixture
def tidal_track():
    with open(DATA_DIR / "test_track_tidal.pkl", "rb") as f:
        return Track.from_tidal(pickle.load(f))


@pytest.fixture
def spotify_track_list():
    tracks = [
        Track(
            track_id="2Wqw8VqMlpNYZTfIsRqYSA",
            artist_ids=["15kBh7iMF03XANu9pcSAdN", "5MUtPjZ8UJxONYzEGZeArf"],
            name="Hymnesia",
            duration=datetime.timedelta(seconds=374, microseconds=345000),
            origin=Origin.SPOTIFY,
        ),
        Track(
            track_id="1uRFqDldISYmGJAESdoi75",
            artist_ids=["11OUxHFoGgo2NDSdT6YiEC"],
            name="Closer",
            duration=datetime.timedelta(seconds=245, microseconds=277000),
            origin=Origin.SPOTIFY,
        ),
        Track(
            track_id="3cefg1pboKTNqgi3k2t62h",
            artist_ids=["1khyIydqanugacJyKdmceT"],
            name="Omnia",
            duration=datetime.timedelta(seconds=393, microseconds=24000),
            origin=Origin.SPOTIFY,
        ),
    ]

    return tracks


@pytest.fixture
def create_playlist(spotify_session):
    title = "Test Playlist"
    description = (
        "This playlist was created by the https://github.com/klepp0/musync project."
    )
    user_id = spotify_session.user.user_id
    spotify_response = spotify_session._client.user_playlist_create(
        user_id,
        title,
        public=False,
        collaborative=False,
        description=description,
    )
    new_playlist = Playlist.from_spotify(spotify_response)

    yield new_playlist

    new_playlist_id = new_playlist.playlist_id
    spotify_session._client.current_user_unfollow_playlist(new_playlist_id)


def test_session_is_logged_in(spotify_session):
    return spotify_session.check_login()


def test_session_user(spotify_session):
    assert isinstance(spotify_session.user, User)


def test_session_playlists(spotify_session):
    assert all(isinstance(p, Playlist) for p in spotify_session.load_playlists())


def test_find_track(spotify_session, tidal_track):
    spotify_track = spotify_session.find_track(tidal_track)
    assert tidal_track.equals(spotify_track)


def test_add_to_playlist(spotify_session, create_playlist, spotify_track_list):
    playlist = create_playlist
    n_tracks_before = playlist.n_tracks
    updated_playlist = spotify_session.add_to_playlist(playlist, spotify_track_list)
    n_tracks_after = updated_playlist.n_tracks

    assert playlist.playlist_id == updated_playlist.playlist_id
    assert n_tracks_before < n_tracks_after
