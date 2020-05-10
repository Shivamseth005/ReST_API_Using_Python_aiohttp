# This is __init__ file for Rest_API_Using_Python_aiohttp
from server.server import Server
import asyncio
import logging
_LOGGER: logging.Logger = logging.getLogger(__name__)


def main():
    _LOGGER.info("starting server")
    server = Server()
    server.load_apis()
    loop = asyncio.get_event_loop()
    loop.create_task(server.start())
    loop.run_forever()


if __name__ == '__main__':
    main()
