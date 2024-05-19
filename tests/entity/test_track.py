from musync.entity import Track

MOCK_SPOTIFY_TRACK_ITEM_RESPONSE = {
    "added_at": "2024-02-10T14:17:45Z",
    "added_by": {
        "external_urls": {"spotify": "https://open.spotify.com/user/1128328774"},
        "href": "https://api.spotify.com/v1/users/1128328774",
        "id": "1128328774",
        "type": "user",
        "uri": "spotify:user:1128328774",
    },
    "is_local": False,
    "primary_color": None,
    "track": {
        "preview_url": "https://p.scdn.co/mp3-preview/07adc4648a48ee15ebf93372aef04464fe4af014?cid=8d58eca80bcc45699299fe48e3044a76",
        "available_markets": ["US", "CA", "GB", "FR", "DE"],
        "explicit": False,
        "type": "track",
        "episode": False,
        "track": True,
        "album": {
            "available_markets": ["US", "CA", "GB", "FR", "DE"],
            "type": "album",
            "album_type": "compilation",
            "href": "https://api.spotify.com/v1/albums/2sYpGtr8LUH2qXeY0lBQc5",
            "id": "2sYpGtr8LUH2qXeY0lBQc5",
            "images": [
                {
                    "url": "https://i.scdn.co/image/ab67616d0000b2737824b728f68d1246b9394a1c",
                    "width": 640,
                    "height": 640,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616d00001e027824b728f68d1246b9394a1c",
                    "width": 300,
                    "height": 300,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616d000048517824b728f68d1246b9394a1c",
                    "width": 64,
                    "height": 64,
                },
            ],
            "name": "Feeling Good: Her Greatest Hits And Remixes",
            "release_date": "2022-02-11",
            "release_date_precision": "day",
            "uri": "spotify:album:2sYpGtr8LUH2qXeY0lBQc5",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/7G1GBhoKtEPnP86X2PvEYO"
                    },
                    "href": "https://api.spotify.com/v1/artists/7G1GBhoKtEPnP86X2PvEYO",
                    "id": "7G1GBhoKtEPnP86X2PvEYO",
                    "name": "Nina Simone",
                    "type": "artist",
                    "uri": "spotify:artist:7G1GBhoKtEPnP86X2PvEYO",
                }
            ],
            "external_urls": {
                "spotify": "https://open.spotify.com/album/2sYpGtr8LUH2qXeY0lBQc5"
            },
            "total_tracks": 26,
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/7G1GBhoKtEPnP86X2PvEYO"
                },
                "href": "https://api.spotify.com/v1/artists/7G1GBhoKtEPnP86X2PvEYO",
                "id": "7G1GBhoKtEPnP86X2PvEYO",
                "name": "Nina Simone",
                "type": "artist",
                "uri": "spotify:artist:7G1GBhoKtEPnP86X2PvEYO",
            },
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/586uxXMyD5ObPuzjtrzO1Q"
                },
                "href": "https://api.spotify.com/v1/artists/586uxXMyD5ObPuzjtrzO1Q",
                "id": "586uxXMyD5ObPuzjtrzO1Q",
                "name": "Sofi Tukker",
                "type": "artist",
                "uri": "spotify:artist:586uxXMyD5ObPuzjtrzO1Q",
            },
        ],
        "disc_number": 1,
        "track_number": 22,
        "duration_ms": 232632,
        "external_ids": {"isrc": "USUM72116178"},
        "external_urls": {
            "spotify": "https://open.spotify.com/track/2yTFrY6qG6l46rfVtQDVim"
        },
        "href": "https://api.spotify.com/v1/tracks/2yTFrY6qG6l46rfVtQDVim",
        "id": "2yTFrY6qG6l46rfVtQDVim",
        "name": "Sinnerman - Sofi Tukker Remix",
        "popularity": 38,
        "uri": "spotify:track:2yTFrY6qG6l46rfVtQDVim",
        "is_local": False,
    },
    "video_thumbnail": {"url": None},
}


def test_track_from_spotify():
    track = Track.from_spotify(MOCK_SPOTIFY_TRACK_ITEM_RESPONSE)

    assert track.track_id == MOCK_SPOTIFY_TRACK_ITEM_RESPONSE["track"]["id"]
    assert (
        track.artist_id == MOCK_SPOTIFY_TRACK_ITEM_RESPONSE["track"]["artists"][0]["id"]
    )
    assert track.name == MOCK_SPOTIFY_TRACK_ITEM_RESPONSE["track"]["name"]
    assert track.date_added == MOCK_SPOTIFY_TRACK_ITEM_RESPONSE["added_at"]
