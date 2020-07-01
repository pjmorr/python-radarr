"""Models for Radarr."""

from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

from .exceptions import RadarrError


def dt_str_to_d(dt_str: str) -> date:
    """Convert ISO-8601 datetime string to datetime object."""
    # utc = True if "Z" in dt_str else False
    # if Python doesn't support long microsecond values
    # dt_str = dt_str[:-1] if utc else dt_str
    # ts_bits = dt_str.split(".", 1)
    # dt_str = "{}.{}".format(ts_bits[0], ts_bits[1][:2])
    # dt_str = f"{dt_str}Z" if utc else dt_str
    # fmt = "%Y-%m-%dT%H:%M:%S.%f" if "." in dt_str else "%Y-%m-%dT%H:%M:%S"

    # fmt = f"{fmt}%z" if utc else fmt
    dt_str = dt_str.split("T")[0]
    return date.fromisoformat(dt_str)


def dt_str_to_dt(dt_str: str) -> date:
    """Convert ISO-8601 datetime string to datetime object."""
    utc = True if "Z" in dt_str else False
    fmt = "%Y-%m-%dT%H:%M:%S.%f" if "." in dt_str else "%Y-%m-%dT%H:%M:%S"

    fmt = f"{fmt}%z" if utc else fmt
    return datetime.strptime(dt_str, fmt)


@dataclass(frozen=True)
class Disk:
    """Object holding disk information from Radarr."""

    label: str
    path: str
    free: int
    total: int

    @staticmethod
    def from_dict(data: dict):
        """Return Disk object from Radarr API response."""
        return Disk(
            label=data.get("label", ""),
            path=data.get("path", ""),
            free=data.get("freeSpace", 0),
            total=data.get("totalSpace", 0),
        )


@dataclass(frozen=True)
class Movie:
    """Object holding episode information from Radarr."""

    imdb_id: int
    tmdb_id: int
    title: str
    sort_title: str
    clean_title: str
    year: int
    overview: str
    in_cinimas: date
    physical_release: date
    status: str
    downloaded: bool
    downloading: bool
    wanted: bool
    has_file: bool
    path: str
    folder_name: str
    monitored: bool
    is_available: bool
    ratings: dict

    @staticmethod
    def from_dict(data: dict):
        """Return Episode object from Radarr API response."""
        in_cinemas = data.get("inCinemas", None)
        in_cinemas = dt_str_to_d(in_cinemas) if in_cinemas else None

        physical_release = data.get('physicalRelease', None)
        physical_release = dt_str_to_d(physical_release) if physical_release else None

        downloaded: bool = data.get('downloaded', False)
        monitored: bool = data.get('monitored', False)
        wanted = True if not downloaded and monitored else False

        return Movie(
            imdb_id=data.get('imdbid'),
            tmdb_id=data.get('tmdbid'),
            title=data.get('title'),
            sort_title=data.get('sortTitle'),
            clean_title=data.get('cleanTitle'),
            year=data.get('year'),
            overview=data.get('overview'),
            in_cinimas=in_cinemas,
            physical_release=physical_release,
            status=data.get('stats'),
            downloaded=downloaded,
            downloading=data.get("downloading", False),
            wanted=wanted,
            has_file=data.get('hasFile', False),
            path=data.get('path'),
            folder_name=data.get('folderName'),
            monitored=monitored,
            is_available=data.get('isAvailable', False),
            ratings=data.get('ratings', {})
        )


@dataclass(frozen=True)
class Info:
    """Object holding information from Radarr."""

    app_name: str
    version: str

    @staticmethod
    def from_dict(data: dict):
        """Return Info object from Radarr API response."""
        return Info(app_name="Radarr", version=data.get("version", "Unknown"))


@dataclass(frozen=True)
class CommandItem:
    """Object holding command item information from Radarr."""

    command_id: int
    name: int
    state: str
    queued: datetime
    started: datetime
    changed: datetime
    priority: str = "unknown"
    trigger: str = "unknown"
    message: str = "Not Provided"
    send_to_client: bool = False

    @staticmethod
    def from_dict(data: dict):
        """Return CommandItem object from Radarr API response."""
        if "started" in data:
            started = data.get("started", None)
        else:
            started = data.get("startedOn", None)

        if "queued" in data:
            queued = data.get("queued", None)
        else:
            queued = started

        if started is not None:
            started = dt_str_to_dt(started)

        if queued is not None:
            queued = dt_str_to_dt(queued)

        changed = data.get("stateChangeTime", None)
        if changed is not None:
            changed = dt_str_to_dt(changed)

        return CommandItem(
            command_id=data.get("id", 0),
            name=data.get("name", "Unknown"),
            state=data.get("state", "unknown"),
            priority=data.get("priority", "unknown"),
            trigger=data.get("trigger", "unknown"),
            message=data.get("message", "Not Provided"),
            send_to_client=data.get("sendUpdatesToClient", False),
            queued=queued,
            started=started,
            changed=changed,
        )


@dataclass(frozen=True)
class QueueItem:
    """Object holding queue item information from Radarr."""

    queue_id: int
    download_id: str
    download_status: str
    title: str
    movie: Movie
    protocol: str
    size_remaining: int
    size: int
    status: str
    eta: datetime
    time_remaining: str

    @staticmethod
    def from_dict(data: dict):
        """Return QueueItem object from Radarr API response."""
        movie_data = data.get("movie", {})

        movie = Movie.from_dict(movie_data)

        eta = data.get("estimatedCompletionTime", None)
        if eta is not None:
            eta = dt_str_to_dt(eta)

        return QueueItem(
            queue_id=data.get("id", 0),
            download_id=data.get("downloadId", ""),
            download_status=data.get("trackedDownloadStatus", "Unknown"),
            title=data.get("title", "Unknown"),
            movie=movie,
            protocol=data.get("protocol", "unknown"),
            size=data.get("size", 0),
            size_remaining=data.get("sizeleft", 0),
            status=data.get("status", "Unknown"),
            eta=eta,
            time_remaining=data.get("timeleft", "00:00:00"),
        )


@dataclass(frozen=True)
class WantedResults:
    """Object holding wanted episode results from Radarr."""

    page: int
    per_page: int
    total: int
    sort_key: str
    sort_dir: str
    movies: List[Movie]

    @staticmethod
    def from_dict(data: dict):
        """Return WantedResults object from Radarr API response."""
        movies = [Movie.from_dict(movie) for movie in data.get("records", [])]

        return WantedResults(
            page=data.get("page", 0),
            per_page=data.get("pageSize", 0),
            total=data.get("totalRecords", 0),
            sort_key=data.get("sortKey", ""),
            sort_dir=data.get("sortDirection", ""),
            movies=movies
        )


class Application:
    """Object holding all information of the Radarr Application."""

    info: Info
    disks: List[Disk] = []

    def __init__(self, data: dict):
        """Initialize an empty Radarr application class."""
        # Check if all elements are in the passed dict, else raise an Error
        if any(k not in data for k in ["info"]):
            raise RadarrError("Radarr data is incomplete, cannot construct object")
        self.update_from_dict(data)

    def update_from_dict(self, data: dict) -> "Application":
        """Return Application object from Radarr API response."""
        if "info" in data and data["info"]:
            self.info = Info.from_dict(data["info"])

        if "diskspace" in data and data["diskspace"]:
            disks = [Disk.from_dict(disk) for disk in data["diskspace"]]
            self.disks = disks

        return self
