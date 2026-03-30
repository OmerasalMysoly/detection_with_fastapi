import os
from fastapi import Request, Response
import logging
import traceback
import json
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

# Define logger
logger = logging.getLogger(__name__)

def log_to_file(request, response, body_bytes=None):
    try:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Method: {request.method}\n")
            f.write(f"URL: {request.url}\n")
            f.write(f"Status: {response.status_code}\n")
            if body_bytes:
                f.write(f"Body: {body_bytes.decode('utf-8', errors='replace')}\n")
            else:
                f.write(f"Body: <Not Captured>\n")
            f.write("-" * 20 + "\n")
    except Exception as log_error:
        # logger is available in the module scope
        logger.error(f"Failed to write to logs.txt: {log_error}")

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        body_bytes = await request.body()

        async def receive():
            return {
                "type": "http.request",
                "body": body_bytes,
                "more_body": False
            }

        request._receive = receive

        token_param = request.query_params.get("secret")

        if request.url.path not in ["/", "/openapi.json", "/status", "/favicon.ico", "/vision-detect"]:
            if not token_param or token_param != SECRET_KEY:
                response = Response("Unauthorized Access", status_code=401)
                log_to_file(request, response, body_bytes)
                return response

        try:
            response = await call_next(request)

            if response.status_code != 200:
                log_to_file(request, response, body_bytes)

            return response

        except Exception:
            response = Response("Internal Server Error", status_code=500)
            log_to_file(request, response, body_bytes)
            return response
