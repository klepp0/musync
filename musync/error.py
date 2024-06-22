class PlaylistNotFoundError(Exception):
    """Raised when a playlist is not found in the database."""


class ConnectionError(Exception):
    """Raised when a connection of a Session is not established."""
