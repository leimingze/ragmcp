"""Tests for log_call middleware decorator."""

import io
import logging

import pytest

from ragmcp.middleware import log_call


class TestLogCallRecordsInputAndOutput:
    """Test log_call decorator logs input and output."""

    def test_log_call_records_input_and_output(self):
        """Log call should record input parameters and return value."""

        # Create a string stream to capture logs
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        # Get the logger and add our handler
        test_logger = logging.getLogger("ragmcp.middleware")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.INFO)

        @log_call
        def add(a, b):
            return a + b

        result = add(2, 3)

        # Clean up
        test_logger.removeHandler(handler)

        assert result == 5
        # Check that log contains the function name and values
        log_output = log_stream.getvalue()
        assert "add" in log_output
        assert "(2, 3)" in log_output or "args=(2, 3)" in log_output
        assert "5" in log_output

    def test_log_call_with_keyword_arguments(self):
        """Log call should handle keyword arguments."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        test_logger = logging.getLogger("ragmcp.middleware")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.INFO)

        @log_call
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")

        test_logger.removeHandler(handler)

        assert result == "Hi, Alice!"
        log_output = log_stream.getvalue()
        assert "greet" in log_output

    def test_log_call_with_no_arguments(self):
        """Log call should handle functions with no arguments."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        test_logger = logging.getLogger("ragmcp.middleware")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.INFO)

        @log_call
        def no_args():
            return "success"

        result = no_args()

        test_logger.removeHandler(handler)

        assert result == "success"
        log_output = log_stream.getvalue()
        assert "no_args" in log_output


class TestLogCallRecordsDuration:
    """Test log_call decorator records execution time."""

    def test_log_call_records_duration(self):
        """Log call should record execution duration in milliseconds."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        test_logger = logging.getLogger("ragmcp.middleware")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.INFO)

        @log_call
        def quick_function():
            return "done"

        quick_function()

        test_logger.removeHandler(handler)

        log_output = log_stream.getvalue()
        # Should contain duration information
        assert "duration" in log_output.lower() or "ms" in log_output.lower()

    def test_log_call_duration_is_positive(self):
        """Duration should always be positive."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        test_logger = logging.getLogger("ragmcp.middleware")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.INFO)

        @log_call
        def return_value():
            return 42

        return_value()

        test_logger.removeHandler(handler)

        log_output = log_stream.getvalue()
        # Should contain a number (duration in ms)
        assert any(char.isdigit() for char in log_output)


class TestLogCallWithError:
    """Test log_call decorator behavior with exceptions."""

    def test_log_call_records_exception(self):
        """Log call should record exceptions."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.ERROR)

        test_logger = logging.getLogger("ragmcp.middleware")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.ERROR)

        @log_call
        def failing_function():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            failing_function()

        test_logger.removeHandler(handler)

        log_output = log_stream.getvalue()
        # Should have logged the error
        assert "ValueError" in log_output or "Test error" in log_output

    def test_log_call_exception_preserves_traceback(self):
        """Exception should be re-raised with original traceback."""

        @log_call
        def raise_error():
            raise ValueError("Original error")

        with pytest.raises(ValueError, match="Original error"):
            raise_error()


class TestLogCallConfiguration:
    """Test log_call decorator configuration options."""

    def test_log_level_debug(self):
        """Should support custom log levels."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.DEBUG)

        test_logger = logging.getLogger("test.debug.logger")
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.DEBUG)

        @log_call(logging.DEBUG, logger_name="test.debug.logger")
        def debug_function():
            return "debug"

        debug_function()

        test_logger.removeHandler(handler)

        log_output = log_stream.getvalue()
        assert "debug_function" in log_output

    def test_log_call_with_logger_name(self):
        """Should support custom logger names."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.INFO)

        custom_logger = logging.getLogger("custom.test.logger")
        custom_logger.addHandler(handler)
        custom_logger.setLevel(logging.INFO)

        @log_call(logger_name="custom.test.logger")
        def custom_logger_function():
            return "result"

        result = custom_logger_function()

        custom_logger.removeHandler(handler)

        assert result == "result"
        log_output = log_stream.getvalue()
        assert "custom_logger_function" in log_output


class TestLogCallPreservesMetadata:
    """Test that log_call decorator preserves function metadata."""

    def test_preserves_function_name(self):
        """Log call decorator should preserve original function name."""

        @log_call
        def my_function():
            return "result"

        assert my_function.__name__ == "my_function"

    def test_preserves_function_docstring(self):
        """Log call decorator should preserve original function docstring."""

        @log_call
        def documented_function():
            """This is a documented function."""
            return "result"

        assert documented_function.__doc__ == "This is a documented function."
