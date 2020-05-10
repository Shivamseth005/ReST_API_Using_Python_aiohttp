import logging
from server.sample import SampleAPI
from aiohttp import web

MAX_CLIENT_SIZE: int = 1
_LOGGER: logging.Logger = logging.getLogger(__name__)


class Server:
    def __init__(self) -> None:
        self._site = None
        self._host = "127.0.0.1"
        self._port = 8080
        self.webapp: web.Application = web.Application(
            client_max_size=MAX_CLIENT_SIZE
            # middlewares=[self.security.token_validation],
            # later we will add this to validate token
        )
        # service stuff
        self._runner: web.AppRunner = web.AppRunner(self.webapp)

    def load_apis(self) -> None:
        sampleapi = SampleAPI()
        self.webapp.add_routes(
            [
                web.get("/host/info", sampleapi.info),
                web.get("/host/stats", sampleapi.stats),
                web.get("/host/data", sampleapi.data),
            ]
        )

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        self._host = host

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, port: str) -> None:
        self._port = int(port)

    async def start(self) -> None:
        """Run RESTful API webserver."""
        await self._runner.setup()
        self._site = web.TCPSite(
            self._runner,
            host="127.0.0.1",
            port=int(self.port),
            shutdown_timeout=5
        )

        try:
            await self._site.start()
        except OSError as err:
            _LOGGER.fatal("Failed to create HTTP server at %s:%s -> %s"
                          % (self.host, self.port, err))
        else:
            _LOGGER.info("Start API on %s:%d" % (self.host, self.port))

    async def stop(self) -> None:
        """Stop RESTful API webserver."""
        if not self._site:
            return

        # Shutdown running API
        await self._site.stop()
        await self._runner.cleanup()

        _LOGGER.info("Stop API on %s:%d" % (self._host, self._port))
