import warnings

# from musync.common.entity import Playlist, Track
from musync.app.models import Playlist, Track
from musync.common.error import MissingPrivilegesError, TrackNotFoundWarning
from musync.spotify.session import SpotifySession
from musync.tidal.session import TidalSession

SessionType = SpotifySession | TidalSession


class SyncManager:
    def __init__(self, session1: SessionType, session2: SessionType) -> None:
        assert isinstance(session1, (SpotifySession, TidalSession))
        assert isinstance(session2, (SpotifySession, TidalSession))
        assert session1 != session2

        self._session1 = session1
        self._session2 = session2

    def get_common_playlists(self) -> list[tuple[Playlist, Playlist]]:
        playlists1 = self._session1.load_playlists()
        playlists2 = self._session2.load_playlists()
        common_playlists = []
        for playlist1 in playlists1:
            for playlist2 in playlists2:
                if playlist1.name == playlist2.name:
                    common_playlists.append((playlist1, playlist2))

        return common_playlists

    def get_missing_tracks(
        self, src_playlist: Playlist, dest_playlist: Playlist
    ) -> list[Track]:
        if src_playlist.origin == self._session1.user.origin:
            src_session = self._session1
        elif src_playlist.origin == self._session2.user.origin:
            src_session = self._session2
        else:
            raise MissingPrivilegesError(
                f"The user does not have access to the source playlist ({src_playlist=})"
            )

        if (
            dest_playlist.origin == self._session1.user.origin
            and dest_playlist.owner_id == self._session1.user.user_id
        ):
            dest_session = self._session1
        elif (
            dest_playlist.origin == self._session2.user.origin
            and dest_playlist.owner_id == self._session2.user.user_id
        ):
            dest_session = self._session2
        else:
            raise MissingPrivilegesError(
                f"The user does not have access to the destination playlist ({dest_playlist=})"
            )

        src_tracks = src_session.load_playlist_tracks(src_playlist)
        dest_tracks = dest_session.load_playlist_tracks(dest_playlist)

        return [st for st in src_tracks if all(not st.equals(dt) for dt in dest_tracks)]

    def sync_common_playlists(self) -> None:
        common_playlists = self.get_common_playlists()

        for src_playlist, dest_playlist in common_playlists:
            if dest_playlist.owner_id == self._session2.user.user_id:
                self.sync_playlists(src_playlist, dest_playlist)

        for dest_playlist, src_playlist in common_playlists:
            if dest_playlist.owner_id == self._session1.user.user_id:
                self.sync_playlists(src_playlist, dest_playlist)

    def sync_playlists(self, src_playlist, dest_playlist) -> Playlist:
        if (
            dest_playlist.origin == self._session1.user.origin
            and dest_playlist.owner_id == self._session1.user.user_id
        ):
            dest_session = self._session1
        elif (
            dest_playlist.origin == self._session2.user.origin
            and dest_playlist.owner_id == self._session2.user.user_id
        ):
            dest_session = self._session2
        else:
            raise MissingPrivilegesError(
                f"The user does not have access to the destination playlist ({dest_playlist=})"
            )

        missing_tracks_src = self.get_missing_tracks(src_playlist, dest_playlist)
        missing_tracks_dest = []
        for src_track in missing_tracks_src:
            if src_track.origin == dest_session.user.origin:
                dest_track = src_track
            else:
                dest_track = dest_session.find_track(src_track)

            if dest_track is None:
                warnings.warn(
                    f"Track {src_track} not found in {dest_session}",
                    TrackNotFoundWarning,
                )
            else:
                missing_tracks_dest.append(dest_track)

        if len(missing_tracks_dest) == 0:
            return dest_playlist

        return dest_session.add_to_playlist(dest_playlist, missing_tracks_dest)
