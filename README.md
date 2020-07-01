# Python: Radarr Client

Asynchronous Python client for Radarr API.

This project was derived from [ctalkington/python-sonarr](https://github.com/ctalkington/python-sonarr) (available via pypi/pip)

Since Sonarr and Radarr were created from the same roots, I figured it would be fitting to derive a python client from one to the other.

## About

This package allows you to monitor a Radarr instance.

## Installation

```bash
pip install radarr
```

## Usage

```python
import asyncio

from radarr import Radarr


async def main():
    """Show example of connecting to your Radarr instance."""
    async with Radarr("192.168.1.100", "API_TOKEN") as radarr:
        # basic: simple api for monitoring purposes only.
        info = await radarr.update()
        print(info)

        calendar = await radarr.calendar()
        print(calendar)

        commands = await radarr.commands()
        print(commands)

        queue = await radarr.queue()
        print(queue)

        series = await radarr.series()
        print(series)

        wanted = await radarr.wanted()
        print(wanted)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
