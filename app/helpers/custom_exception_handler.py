from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncio
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.types import ASGIApp
from typing import Any, Dict, List, Tuple, Union

from pydantic_core import ErrorDetails
from pydantic import BaseModel, HttpUrl, ValidationError

import json

async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )

def loc_to_dot_sep(loc: Tuple[Union[str, int], ...]) -> str:
    path = ''
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += ', '
            path += x
        elif isinstance(x, int):
            path += f'[{x}]'
        else:
            raise TypeError('Unexpected type')
    return path

def convert_errors(e: ValidationError) -> List[Dict[str, Any]]:
    new_errors: List[Dict[str, Any]] = e.errors()
    formatted_message = e.errors()
    for error in new_errors:
        error['loc'] = loc_to_dot_sep(error['loc'])
    return new_errors

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()
    modified_details = []
    # Replace 'msg' with 'message' for each error
    for error in details:
        modified_details.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )

async def chat_error_message():
    for chunk in ["Please", "try","with","another","question"]:
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"  
        # await asyncio.sleep(0.1)  # simulate streaming