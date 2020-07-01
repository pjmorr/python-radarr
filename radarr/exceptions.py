"""Exceptions for Radarr."""


class RadarrError(Exception):
    """Generic Radarr Exception."""

    pass


class RadarrConnectionError(RadarrError):
    """Radarr connection exception."""

    pass


class RadarrAccessRestricted(RadarrError):
    """Radarr access restricted exception."""

    pass


class RadarrResourceNotFound(RadarrError):
    """Radarr resource not found exception."""

    pass
