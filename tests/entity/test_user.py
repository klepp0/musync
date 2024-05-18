from musync.entity import User

MOCK_SPOTIFY_USER_RESPONSE = {
    "display_name": "Jane Doe",
    "external_urls": {"spotify": "https://open.spotify.com/user/9876543210"},
    "href": "https://api.spotify.com/v1/users/9876543210",
    "id": "9876543210",
    "images": [
        {
            "url": "https://i.scdn.co/image/ab67757000003b821234567890abcdef12345678",
            "height": 64,
            "width": 64,
        },
        {
            "url": "https://i.scdn.co/image/ab6775700000ee851234567890abcdef12345678",
            "height": 300,
            "width": 300,
        },
    ],
    "type": "user",
    "uri": "spotify:user:9876543210",
    "followers": {"href": None, "total": 42},
}


def test_user_from_spotify():
    user = User.from_spotify(MOCK_SPOTIFY_USER_RESPONSE)

    assert user.user_id == MOCK_SPOTIFY_USER_RESPONSE["id"]
    assert user.name == MOCK_SPOTIFY_USER_RESPONSE["display_name"]
