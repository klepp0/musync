from musync.entity import Playlist

MOCK_SPOTIFY_PLAYLIST_ITEM_RESPONSE = {
    "collaborative": False,
    "description": "A mix of upbeat and relaxing tunes.",
    "external_urls": {"spotify": "https://open.spotify.com/playlist/mockPlaylistId"},
    "href": "https://api.spotify.com/v1/playlists/mockPlaylistId",
    "id": "mockPlaylistId",
    "images": [{"height": 640, "url": "https://via.placeholder.com/640", "width": 640}],
    "name": "Mock Playlist 🎶",
    "owner": {
        "display_name": "Mock User",
        "external_urls": {"spotify": "https://open.spotify.com/user/mockUserId"},
        "href": "https://api.spotify.com/v1/users/mockUserId",
        "id": "mockUserId",
        "type": "user",
        "uri": "spotify:user:mockUserId",
    },
    "primary_color": None,
    "public": True,
    "snapshot_id": "mockSnapshotId",
    "tracks": {
        "href": "https://api.spotify.com/v1/playlists/mockPlaylistId/tracks",
        "total": 10,
    },
    "type": "playlist",
    "uri": "spotify:playlist:mockPlaylistId",
}


def test_playlist_from_spotify():
    playlist = Playlist.from_spotify(MOCK_SPOTIFY_PLAYLIST_ITEM_RESPONSE)

    assert playlist.playlist_id == MOCK_SPOTIFY_PLAYLIST_ITEM_RESPONSE["id"]
    assert playlist.owner_id == MOCK_SPOTIFY_PLAYLIST_ITEM_RESPONSE["owner"]["id"]
    assert playlist.name == MOCK_SPOTIFY_PLAYLIST_ITEM_RESPONSE["name"]
