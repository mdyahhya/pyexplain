"""
Core Functionality Tests for PyExplain

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pytest
import pyexplain
from pyexplain.core import (
    decode_traceback,
    decode_exception,
    safe_run,
    format_decoded_output
)
from tests import SAMPLE_TRACEBACKS, create_test_exception, TestHelper


class TestDecodeTraceback:
    """Tests for decode_traceback() function."""
    
    def test_decode_traceback_basic(self):
        """Test basic traceback decoding."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb)
        
        TestHelper.assert_valid_decoded_output(result)
        assert result['error_type'] == 'ValueError'
        assert result['success'] is False
    
    def test_decode_traceback_zero_division(self):
        """Test ZeroDivisionError decoding."""
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        result = decode_traceback(tb)
        
        assert result['error_type'] == 'ZeroDivisionError'
        assert 'zero' in result['simple_explanation'].lower()
    
    def test_decode_traceback_with_branding(self):
        """Test that branding is included by default."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb, add_branding=True)
        
        assert result['branding'] is not None
        TestHelper.assert_contains_branding(result['branding'])
    
    def test_decode_traceback_without_branding(self):
        """Test branding can be disabled."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb, add_branding=False)
        
        assert result['branding'] is None


class TestDecodeException:
    """Tests for decode_exception() function."""
    
    def test_decode_exception_basic(self):
        """Test basic exception decoding."""
        exc = create_test_exception(ValueError, "test value error")
        result = decode_exception(exc)
        
        TestHelper.assert_valid_decoded_output(result)
        assert result['error_type'] == 'ValueError'


class TestSafeRun:
    """Tests for safe_run() function."""
    
    def test_safe_run_success(self):
        """Test successful code execution."""
        code = "x = 10\ny = 20\nresult = x + y"
        result = safe_run(code)
        
        assert result['success'] is True
    
    def test_safe_run_with_error(self):
        """Test error handling in safe_run."""
        code = "x = 10 / 0"
        result = safe_run(code)
        
        assert result['success'] is False
        assert result['error_type'] == 'ZeroDivisionError'


class TestFormatDecodedOutput:
    """Tests for format_decoded_output() function."""
    
    def test_format_decoded_output_basic(self):
        """Test basic formatting."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        decoded = decode_traceback(tb)
        formatted = format_decoded_output(decoded)
        
        assert isinstance(formatted, str)
        assert 'ValueError' in formatted


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
