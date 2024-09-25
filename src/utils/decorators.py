import functools
import time
from collections.abc import Callable
from typing import Any

from anthropic import (
    AnthropicError,
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

from src.utils.logger import logger


def base_error_handler(logger=logger):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


def application_level_handler():
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print("\nUser terminated program execution\n")
            except SystemExit:
                print("\nExit application\n")
            except Exception as e:
                print(f"Error in {func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


def anthropic_error_handler(logger=logger):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except AuthenticationError as e:
                logger.error(f"Authentication failed in {func.__name__}: {str(e)}")
                raise
            except BadRequestError as e:
                logger.error(f"Invalid request in {func.__name__}: {str(e)}")
                raise
            except PermissionDeniedError as e:
                logger.error(f"Permission denied in {func.__name__}: {str(e)}")
                raise
            except NotFoundError as e:
                logger.error(f"Resource not found in {func.__name__}: {str(e)}")
                raise
            except RateLimitError as e:
                logger.warning(f"Rate limit exceeded in {func.__name__}: {str(e)}")
                raise
            except APIConnectionError as e:
                if isinstance(e, APITimeoutError):
                    logger.error(f"Request timed out in {func.__name__}: {str(e)}")
                else:
                    logger.error(f"Connection error in {func.__name__}: {str(e)}")
                raise
            except InternalServerError as e:
                logger.error(f"Anthropic internal server error in {func.__name__}: {str(e)}")
                raise
            except APIError as e:
                logger.error(f"Unexpected API error in {func.__name__}: {str(e)}")
                raise
            except AnthropicError as e:
                logger.error(f"Unexpected Anthropic error in {func.__name__}: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}")

        return wrapper

    return decorator


def performance_logger(logger=logger):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.debug(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
            return result

        return wrapper

    return decorator
