from typing import (
    Optional,
    Any,
    Dict,
)
from exceptions.exceptions import (
    ServerException,
    APIError,
    APIForbidden,
)
from .const import (
    JSON_MESSAGE,
    JSON_DATA,
    JSON_RESULT,
    RESULT_OK,
    RESULT_ERROR,
)
from aiohttp import web


def api_return_error(message: Optional[str] = None) -> web.Response:
    """Return an API error message."""
    return web.json_response(
        {JSON_RESULT: RESULT_ERROR, JSON_MESSAGE: message}, status=400
    )


def api_return_ok(data: Optional[Dict[str, Any]] = None) -> web.Response:
    """Return an API ok answer."""
    return web.json_response({JSON_RESULT: RESULT_OK, JSON_DATA: data or {}})


def api_process(method):
    """Wrap function with true/false calls to rest api."""

    async def wrap_api(api, *args, **kwargs):
        """Return API information."""
        try:
            answer = await method(api, *args, **kwargs)
        except (APIError, APIForbidden) as err:
            return api_return_error(message=str(err))
        except ServerException:
            return api_return_error(message="Unknown Error, see logs")

        if isinstance(answer, dict):
            return api_return_ok(data=answer)
        if isinstance(answer, web.Response):
            return answer
        elif isinstance(answer, bool) and not answer:
            return api_return_error()
        return api_return_ok()

    return wrap_api
