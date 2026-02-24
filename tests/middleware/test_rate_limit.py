"""Tests for rate_limit middleware decorator."""

import time

from ragmcp.middleware import rate_limit


class TestRateLimitWaitsWhenExceeded:
    """Test rate_limit decorator enforces rate limits."""

    def test_rate_limit_waits_when_exceeded(self):
        """When rate limit exceeded, should wait until next window."""

        call_times = []

        @rate_limit(max_requests=2, time_window=0.1)
        def tracked_call():
            call_times.append(time.time())

        # First 2 calls should proceed immediately
        tracked_call()
        tracked_call()

        # 3rd call should wait for next time window
        start = time.time()
        tracked_call()
        elapsed = time.time() - start

        assert len(call_times) == 3
        # Should have waited at least time_window seconds
        assert elapsed >= 0.1

    def test_rate_limit_resets_after_window(self):
        """After time_window passes, rate limit should reset."""

        call_count = 0

        @rate_limit(max_requests=2, time_window=0.1)
        def count_calls():
            nonlocal call_count
            call_count += 1

        # Use up the rate limit
        count_calls()
        count_calls()

        # Wait for window to pass
        time.sleep(0.15)

        # Should be able to make 2 more calls
        count_calls()
        count_calls()

        assert call_count == 4

    def test_consecutive_calls_within_limit(self):
        """Calls within rate limit should proceed without delay."""

        call_times = []

        @rate_limit(max_requests=5, time_window=1.0)
        def tracked_call():
            call_times.append(time.time())

        start = time.time()
        for _ in range(5):
            tracked_call()
        elapsed = time.time() - start

        assert len(call_times) == 5
        # Should complete very quickly with no waiting
        assert elapsed < 0.05


class TestRateLimitConfiguration:
    """Test rate_limit decorator configuration options."""

    def test_custom_max_requests(self):
        """Should respect custom max_requests parameter."""

        call_count = 0

        @rate_limit(max_requests=3, time_window=1.0)
        def count_calls():
            nonlocal call_count
            call_count += 1

        # Should be able to make 3 calls
        count_calls()
        count_calls()
        count_calls()

        assert call_count == 3

    def test_custom_time_window(self):
        """Should respect custom time_window parameter."""

        call_times = []

        @rate_limit(max_requests=1, time_window=0.05)
        def tracked_call():
            call_times.append(time.time())

        tracked_call()

        # Second call should wait
        start = time.time()
        tracked_call()
        elapsed = time.time() - start

        assert elapsed >= 0.05

    def test_single_request_no_limit(self):
        """max_requests=1 means one call per time window."""

        call_times = []

        @rate_limit(max_requests=1, time_window=0.1)
        def tracked_call():
            call_times.append(time.time())

        tracked_call()
        tracked_call()

        assert len(call_times) == 2
        delay = call_times[1] - call_times[0]
        assert delay >= 0.1


class TestRateLimitThreadSafety:
    """Test rate_limit behavior with multiple calls."""

    def test_sequential_calls_obey_limit(self):
        """Sequential calls should obey the rate limit."""

        call_times = []

        @rate_limit(max_requests=2, time_window=0.1)
        def tracked_call():
            call_times.append(time.time())

        # Make 4 calls - should take at least 1 time_window
        start = time.time()
        tracked_call()  # 1
        tracked_call()  # 2
        tracked_call()  # 3 - waits
        tracked_call()  # 4 - waits
        elapsed = time.time() - start

        assert len(call_times) == 4
        # Should have waited at least once
        assert elapsed >= 0.1


class TestRateLimitPreservesMetadata:
    """Test that rate_limit decorator preserves function metadata."""

    def test_preserves_function_name(self):
        """Rate limit decorator should preserve original function name."""

        @rate_limit(max_requests=3)
        def my_function():
            return "result"

        assert my_function.__name__ == "my_function"

    def test_preserves_function_docstring(self):
        """Rate limit decorator should preserve original function docstring."""

        @rate_limit(max_requests=3)
        def documented_function():
            """This is a documented function."""
            return "result"

        assert documented_function.__doc__ == "This is a documented function."

    def test_preserves_return_value(self):
        """Rate limit decorator should preserve return value."""

        @rate_limit(max_requests=3, time_window=1.0)
        def return_value():
            return "test_result"

        result = return_value()
        assert result == "test_result"

    def test_preserves_arguments(self):
        """Rate limit decorator should preserve function arguments."""

        @rate_limit(max_requests=3, time_window=1.0)
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5
