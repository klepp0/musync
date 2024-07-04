class PlaylistNotFoundError(Exception):
    """Raised when a playlist is not found in the database."""


class MissingPrivilegesError(Exception):
    """Raised when a user does not have the necessary privileges."""


class IncompatibleEntityError(Exception):
    """Raised when an entity is not compatible with the operation."""
