import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('employees')


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        logger.info(
            f"REQUEST {request.method} {request.path} | "
            f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'}"
        )
        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"RESPONSE {request.method} {request.path} | "
                f"Status: {response.status_code} | Time: {duration:.3f}s"
            )
            response['X-Response-Time'] = f"{duration:.3f}s"
        return response

    def process_exception(self, request, exception):
        logger.error(
            f"EXCEPTION {request.method} {request.path} | Error: {exception}",
            exc_info=True,
        )
        return None
