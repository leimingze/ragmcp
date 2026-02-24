"""Tests for retry middleware decorator."""

import time

import pytest

from ragmcp.middleware import retry


class TestRetryOnNetworkError:
    """Test retry decorator handles network errors."""

    def test_retry_on_connection_error(self):
        """Retry decorator should retry on ConnectionError."""

        call_count = 0

        @retry(max_attempts=3, backoff_factor=0)
        def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Network error")
            return "success"

        result = failing_function()

        assert result == "success"
        assert call_count == 3

    def test_retry_on_timeout(self):
        """Retry decorator should retry on Timeout."""

        call_count = 0

        @retry(max_attempts=3, backoff_factor=0)
        def timeout_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TimeoutError("Request timeout")
            return "success"

        result = timeout_function()

        assert result == "success"
        assert call_count == 2

    def test_retry_respects_custom_exceptions(self):
        """Retry decorator should retry on specified exceptions."""

        call_count = 0

        class CustomError(Exception):
            pass

        @retry(max_attempts=3, exceptions=(CustomError,))
        def custom_error_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise CustomError("Custom error")
            return "success"

        result = custom_error_function()

        assert result == "success"
        assert call_count == 3

    def test_no_retry_on_unspecified_exception(self):
        """Retry decorator should not retry on unspecified exceptions."""

        call_count = 0

        @retry(max_attempts=3, exceptions=(ConnectionError,))
        def value_error_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Should not retry")

        with pytest.raises(ValueError):
            value_error_function()

        assert call_count == 1


class TestMaxRetriesExceeded:
    """Test retry behavior when max retries is exceeded."""

    def test_max_retries_exceeded_raises_error(self):
        """When max retries exceeded, original exception should be raised."""

        @retry(max_attempts=3, backoff_factor=0)
        def always_failing_function():
            raise ConnectionError("Always fails")

        with pytest.raises(ConnectionError, match="Always fails"):
            always_failing_function()

    def test_default_max_attempts_is_three(self):
        """Default max_attempts should be 3."""

        call_count = 0

        @retry(backoff_factor=0)
        def count_calls():
            nonlocal call_count
            call_count += 1
            raise ConnectionError("Fail")

        with pytest.raises(ConnectionError):
            count_calls()

        # Should be called 3 times (initial + 2 retries)
        assert call_count == 3


class TestRetryBackoff:
    """Test exponential backoff behavior."""

    def test_exponential_backoff(self):
        """Retry should use exponential backoff between attempts."""

        call_times = []

        @retry(max_attempts=3, backoff_factor=0.01)
        def backoff_function():
            call_times.append(time.time())
            if len(call_times) < 3:
                raise ConnectionError("Network error")
            return "success"

        backoff_function()

        assert len(call_times) == 3
        # Check that delays increase (exponential backoff)
        delay1 = call_times[1] - call_times[0]
        delay2 = call_times[2] - call_times[1]
        # Second delay should be longer than first
        assert delay2 > delay1

    def test_zero_backoff_factor_no_delay(self):
        """With backoff_factor=0, retries should happen immediately."""

        call_count = 0

        @retry(max_attempts=5, backoff_factor=0)
        def immediate_retry():
            nonlocal call_count
            call_count += 1
            if call_count < 5:
                raise ConnectionError("Fail")
            return "success"

        start = time.time()
        result = immediate_retry()
        elapsed = time.time() - start

        assert result == "success"
        assert call_count == 5
        # Should complete very quickly with no backoff
        assert elapsed < 0.1


class TestRetryConfiguration:
    """Test retry decorator configuration options."""

    def test_custom_max_attempts(self):
        """Should respect custom max_attempts parameter."""

        call_count = 0

        @retry(max_attempts=5, backoff_factor=0)
        def five_attempts():
            nonlocal call_count
            call_count += 1
            if call_count < 5:
                raise ConnectionError("Fail")
            return "success"

        result = five_attempts()

        assert result == "success"
        assert call_count == 5

    def test_single_attempt_no_retry(self):
        """max_attempts=1 means no retry."""

        call_count = 0

        @retry(max_attempts=1, backoff_factor=0)
        def no_retry():
            nonlocal call_count
            call_count += 1
            raise ConnectionError("Fail")

        with pytest.raises(ConnectionError):
            no_retry()

        assert call_count == 1


class TestRetryPreservesFunctionMetadata:
    """Test that retry decorator preserves function metadata."""

    def test_preserves_function_name(self):
        """Retry decorator should preserve original function name."""

        @retry(max_attempts=3)
        def my_function():
            return "result"

        assert my_function.__name__ == "my_function"

    def test_preserves_function_docstring(self):
        """Retry decorator should preserve original function docstring."""

        @retry(max_attempts=3)
        def documented_function():
            """This is a documented function."""
            return "result"

        assert documented_function.__doc__ == "This is a documented function."
