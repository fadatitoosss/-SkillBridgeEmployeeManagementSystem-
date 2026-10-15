import functools, logging, time

logger = logging.getLogger(__name__)

def log_view_action(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user.username if request.user.is_authenticated else "anonymous"
        logger.info("START %s by %s", view_func.__name__, user)
        start = time.time()
        response = view_func(request, *args, **kwargs)
        logger.info("END %s status=%s %sms", view_func.__name__,
                    response.status_code, round((time.time() - start) * 1000, 2))
        return response
    return wrapper