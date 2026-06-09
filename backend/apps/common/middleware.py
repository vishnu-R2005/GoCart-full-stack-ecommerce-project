import logging
import time
import uuid

logger = logging.getLogger('gocart')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())[:8]
        request.request_id = request_id
        start = time.time()

        response = self.get_response(request)

        duration_ms = round((time.time() - start) * 1000, 2)
        logger.info(
            f'{request.method} {request.path} {response.status_code} {duration_ms}ms',
            extra={'request_id': request_id},
        )
        response['X-Request-ID'] = request_id
        return response
