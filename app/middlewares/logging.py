from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            start = time.time()

            response = await call_next(request)

            duration = time.time() - start

            logger.info(f"{request.method} {request.url} - {duration:.4f}s")

            return response
        
        except Exception as e:
            logger.info(f"Error: {e}")
            print(f"[ERROR] {e}")
            raise e