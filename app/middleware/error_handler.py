from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import NotFoundError, UnauthorizedError, BadRequestError


def register_error_handler(app):

    @app.exception_handler(NotFoundError)
    async def handle_not_found(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"message": exc.msg})

    @app.exception_handler(UnauthorizedError)
    async def handle_unauthorized(request: Request, exc: UnauthorizedError):
        return JSONResponse(status_code=401, content={"message": exc.msg})

    @app.exception_handler(BadRequestError)
    async def handle_bad_request(request: Request, exc: BadRequestError):
        return JSONResponse(status_code=400, content={"message": exc.msg})

    @app.exception_handler(Exception)
    async def handle_unknown(request: Request, exc: Exception):
        print("co loi:", exc)
        return JSONResponse(status_code=500, content={"message": "Internal Server"})