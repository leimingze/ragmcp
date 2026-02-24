"""Middleware decorators for RAG MCP.

This module provides middleware decorators for LLM/Embedding calls,
including retry logic, rate limiting, and logging.
"""

import functools
import logging
import threading
import time
from collections import defaultdict, deque
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")

# Thread-safe storage for rate limiting state
_rate_limit_state = defaultdict(deque)  # type: defaultdict[str, deque[float]]
_rate_limit_lock = threading.Lock()

# Module logger
logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    backoff_factor: float = 0.5,
    exceptions: tuple[type[Exception], ...] = (
        ConnectionError,
        TimeoutError,
    ),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to retry a function on specific exceptions.

    Args:
        max_attempts: Maximum number of attempts (including initial call).
                      Default is 3.
        backoff_factor: Multiplier for exponential backoff delay between retries.
                        Delay is calculated as: backoff_factor * (2 ** attempt_number).
                        Set to 0 for immediate retries.
        exceptions: Tuple of exception types to catch and retry on.
                    Default is (ConnectionError, TimeoutError).

    Returns:
        Decorated function that will retry on specified exceptions.

    Raises:
        The original exception if max_attempts is exceeded.

    Example:
        @retry(max_attempts=3, backoff_factor=0.5)
        def fetch_data():
            # May raise ConnectionError or TimeoutError
            return api_call()
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # Don't sleep after the last attempt
                    if attempt < max_attempts - 1:
                        # Calculate exponential backoff delay
                        delay = backoff_factor * (2**attempt)
                        if delay > 0:
                            time.sleep(delay)

            # If we get here, all attempts failed
            assert last_exception is not None
            raise last_exception

        return wrapper

    return decorator


def rate_limit(
    max_requests: int = 10,
    time_window: float = 1.0,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to rate limit function calls.

    Limits the number of calls to a function within a sliding time window.
    Uses the token bucket algorithm with sliding window tracking.

    Args:
        max_requests: Maximum number of requests allowed within time_window.
        time_window: Time window in seconds for rate limiting.

    Returns:
        Decorated function that will wait if rate limit is exceeded.

    Example:
        @rate_limit(max_requests=10, time_window=1.0)
        def api_call():
            # Will be limited to 10 calls per second
            return service.request()
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Use function's qualified name as key for rate limiting
        func_key = f"{func.__qualname__}_{id(func)}"

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            with _rate_limit_lock:
                call_history = _rate_limit_state[func_key]
                now = time.time()

                # Remove calls outside the time window
                while call_history and call_history[0] < now - time_window:
                    call_history.popleft()

                # If at limit, calculate wait time
                if len(call_history) >= max_requests:
                    oldest_call = call_history[0]
                    wait_time = time_window - (now - oldest_call)

                    if wait_time > 0:
                        # Release lock while waiting
                        _rate_limit_lock.release()
                        try:
                            time.sleep(wait_time)
                            now = time.time()  # Update time after sleep
                        finally:
                            _rate_limit_lock.acquire()

                        # Clean up old calls again after waiting
                        while call_history and call_history[0] < now - time_window:
                            call_history.popleft()

                # Record this call
                call_history.append(now)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_call(
    level_or_func: int | Callable[..., T] | None = None,
    logger_name: str | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to log function calls with input, output, and duration.

    Logs function name, arguments, return value, and execution time.

    Can be used with or without arguments:
        @log_call
        def func(): ...

        @log_call(level=logging.DEBUG, logger_name="my.logger")
        def func(): ...

    Args:
        level_or_func: Logging level to use, or the function to decorate if called
                       without arguments. Default is logging.INFO.
        logger_name: Name of logger to use. If None, uses module logger.

    Returns:
        Decorated function that logs each call.

    Example:
        @log_call(level=logging.DEBUG)
        def process_data(data):
            return transform(data)
    """
    # Handle @log_call without parentheses
    if callable(level_or_func):
        # Called as @log_call
        func = level_or_func
        return _create_log_wrapper(func, logging.INFO, logger_name)

    # Called as @log_call(...) with arguments
    level = level_or_func if level_or_func is not None else logging.INFO

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return _create_log_wrapper(func, level, logger_name)

    return decorator


def _create_log_wrapper(
    func: Callable[..., T],
    level: int,
    logger_name: str | None,
) -> Callable[..., T]:
    """Create a logging wrapper for a function.

    Args:
        func: The function to wrap.
        level: Logging level to use.
        logger_name: Name of logger to use.

    Returns:
        Wrapped function that logs each call.
    """
    # Use provided logger or module logger
    func_logger = logging.getLogger(logger_name) if logger_name else logger

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        func_name = func.__name__

        # Log input
        func_logger.log(
            level,
            f"Calling {func_name} with input: args={args}, kwargs={kwargs}",
        )

        # Execute and time
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000

            # Log output and duration
            func_logger.log(
                level,
                f"{func_name} output: {result!r}, duration: {duration_ms:.2f}ms",
            )

            return result
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            # Log error and duration
            func_logger.error(
                f"{func_name} error: {type(e).__name__}: {e}, duration: {duration_ms:.2f}ms"
            )
            raise

    return wrapper


__all__ = ["retry", "rate_limit", "log_call"]
