"""
Core Functionality Tests for pyDecode

Tests for:
    - decode_traceback()
    - decode_exception()
    - safe_run()
    - format_decoded_output()

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pytest
import sys
from io import StringIO

import pydecode
from pydecode.core import (
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
        assert 'value' in result['simple_explanation'].lower()
    
    def test_decode_traceback_zero_division(self):
        """Test ZeroDivisionError decoding."""
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        result = decode_traceback(tb)
        
        assert result['error_type'] == 'ZeroDivisionError'
        assert 'zero' in result['simple_explanation'].lower()
        assert 'divide' in result['simple_explanation'].lower()
    
    def test_decode_traceback_syntax_error(self):
        """Test SyntaxError decoding."""
        tb = SAMPLE_TRACEBACKS['SyntaxError']
        result = decode_traceback(tb)
        
        assert result['error_type'] == 'SyntaxError'
        assert 'syntax' in result['tags']
        assert 'syntax_details' in result  # Should have extra syntax details
    
    def test_decode_traceback_with_line_number(self):
        """Test extraction of line numbers."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb)
        
        assert result['line_number'] is not None
        assert isinstance(result['line_number'], int)
        assert result['line_number'] > 0
    
    def test_decode_traceback_with_file_name(self):
        """Test extraction of file names."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb)
        
        assert result['file_name'] is not None
        assert 'test.py' in result['file_name']
    
    def test_decode_traceback_empty_input(self):
        """Test handling of empty input."""
        result = decode_traceback("")
        
        assert result['error_type'] == 'InvalidInput'
        assert result['success'] is False
    
    def test_decode_traceback_none_input(self):
        """Test handling of None input."""
        result = decode_traceback(None)
        
        assert result['error_type'] == 'InvalidInput'
        assert result['success'] is False
    
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
    
    def test_decode_traceback_multiple_errors(self):
        """Test decoding multiple different error types."""
        error_types = ['KeyError', 'IndexError', 'NameError', 'TypeError']
        
        for error_type in error_types:
            tb = SAMPLE_TRACEBACKS[error_type]
            result = decode_traceback(tb)
            
            assert result['error_type'] == error_type
            TestHelper.assert_valid_decoded_output(result)
    
    def test_decode_traceback_has_emoji(self):
        """Test that decoded output includes emoji."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb)
        
        assert result['emoji'] is not None
        assert len(result['emoji']) > 0
    
    def test_decode_traceback_has_tags(self):
        """Test that decoded output includes classification tags."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb)
        
        assert isinstance(result['tags'], list)
        assert len(result['tags']) > 0
        assert all(isinstance(tag, str) for tag in result['tags'])
    
    def test_decode_traceback_has_category(self):
        """Test that errors are categorized."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        result = decode_traceback(tb)
        
        assert result['category'] is not None
        assert 'Error' in result['category']


class TestDecodeException:
    """Tests for decode_exception() function."""
    
    def test_decode_exception_basic(self):
        """Test basic exception decoding."""
        exc = create_test_exception(ValueError, "test value error")
        result = decode_exception(exc)
        
        TestHelper.assert_valid_decoded_output(result)
        assert result['error_type'] == 'ValueError'
    
    def test_decode_exception_zero_division(self):
        """Test ZeroDivisionError exception."""
        exc = create_test_exception(ZeroDivisionError, "division by zero")
        result = decode_exception(exc)
        
        assert result['error_type'] == 'ZeroDivisionError'
        assert 'zero' in result['simple_explanation'].lower()
    
    def test_decode_exception_type_error(self):
        """Test TypeError exception."""
        exc = create_test_exception(TypeError, "type mismatch")
        result = decode_exception(exc)
        
        assert result['error_type'] == 'TypeError'
        assert 'type' in result['simple_explanation'].lower()
    
    def test_decode_exception_invalid_input(self):
        """Test handling of invalid input."""
        result = decode_exception("not an exception")
        
        assert result['error_type'] == 'InvalidInput'
        assert result['success'] is False
    
    def test_decode_exception_with_branding(self):
        """Test branding in exception decoding."""
        exc = create_test_exception(ValueError)
        result = decode_exception(exc, add_branding=True)
        
        assert result['branding'] is not None


class TestSafeRun:
    """Tests for safe_run() function."""
    
    def test_safe_run_success(self):
        """Test successful code execution."""
        code = "x = 10\ny = 20\nresult = x + y"
        result = safe_run(code)
        
        assert result['success'] is True
        assert 'output' in result
    
    def test_safe_run_with_output(self):
        """Test capturing print output."""
        code = "print('Hello, World!')"
        result = safe_run(code)
        
        assert result['success'] is True
        assert 'Hello, World!' in result['output']
    
    def test_safe_run_with_error(self):
        """Test error handling in safe_run."""
        code = "x = 10 / 0"
        result = safe_run(code)
        
        assert result['success'] is False
        assert result['error_type'] == 'ZeroDivisionError'
        TestHelper.assert_valid_decoded_output(result)
    
    def test_safe_run_syntax_error(self):
        """Test handling of syntax errors."""
        code = "if x == 5\n    print('missing colon')"
        result = safe_run(code)
        
        assert result['success'] is False
        assert result['error_type'] == 'SyntaxError'
    
    def test_safe_run_name_error(self):
        """Test handling of name errors."""
        code = "print(undefined_variable)"
        result = safe_run(code)
        
        assert result['success'] is False
        assert result['error_type'] == 'NameError'
    
    def test_safe_run_empty_code(self):
        """Test handling of empty code."""
        result = safe_run("")
        
        assert result['success'] is False
        assert result['error_type'] == 'InvalidInput'
    
    def test_safe_run_none_code(self):
        """Test handling of None code."""
        result = safe_run(None)
        
        assert result['success'] is False
        assert result['error_type'] == 'InvalidInput'
    
    def test_safe_run_with_custom_filename(self):
        """Test custom filename in traceback."""
        code = "x = 10 / 0"
        result = safe_run(code, filename="custom_script.py")
        
        assert result['success'] is False
        assert 'custom_script.py' in result.get('file_name', '')
    
    def test_safe_run_output_before_error(self):
        """Test capturing output before error occurs."""
        code = "print('Before error')\nx = 10 / 0\nprint('After error')"
        result = safe_run(code)
        
        assert result['success'] is False
        assert 'Before error' in result['output']
        assert 'After error' not in result['output']


class TestFormatDecodedOutput:
    """Tests for format_decoded_output() function."""
    
    def test_format_decoded_output_basic(self):
        """Test basic formatting."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        decoded = decode_traceback(tb)
        formatted = format_decoded_output(decoded)
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        assert 'ValueError' in formatted
        assert decoded['simple_explanation'] in formatted
    
    def test_format_decoded_output_with_technical(self):
        """Test formatting with technical details."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        decoded = decode_traceback(tb)
        formatted = format_decoded_output(decoded, include_technical=True)
        
        assert 'Technical Details' in formatted
        assert 'Category' in formatted
    
    def test_format_decoded_output_without_technical(self):
        """Test formatting without technical details."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        decoded = decode_traceback(tb)
        formatted = format_decoded_output(decoded, include_technical=False)
        
        assert 'Technical Details' not in formatted
    
    def test_format_decoded_output_with_branding(self):
        """Test formatting includes branding."""
        tb = SAMPLE_TRACEBACKS['ValueError']
        decoded = decode_traceback(tb, add_branding=True)
        formatted = format_decoded_output(decoded)
        
        TestHelper.assert_contains_branding(formatted)
    
    def test_format_decoded_output_invalid_input(self):
        """Test handling of invalid input."""
        formatted = format_decoded_output(None)
        assert 'Invalid' in formatted
        
        formatted = format_decoded_output({})
        assert 'Invalid' in formatted


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_full_workflow_traceback(self):
        """Test complete workflow from traceback to formatted output."""
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        decoded = decode_traceback(tb)
        formatted = format_decoded_output(decoded)
        
        assert decoded['success'] is False
        assert 'ZeroDivisionError' in formatted
        TestHelper.assert_contains_branding(formatted)
    
    def test_full_workflow_exception(self):
        """Test complete workflow from exception to formatted output."""
        exc = create_test_exception(KeyError, "'missing'")
        decoded = decode_exception(exc)
        formatted = format_decoded_output(decoded)
        
        assert decoded['error_type'] == 'KeyError'
        assert 'KeyError' in formatted
    
    def test_full_workflow_safe_run(self):
        """Test complete workflow with safe_run."""
        code = "my_list = [1, 2, 3]\nprint(my_list[10])"
        result = safe_run(code)
        formatted = format_decoded_output(result)
        
        assert result['success'] is False
        assert result['error_type'] == 'IndexError'
        assert 'IndexError' in formatted


# Mark slow tests
@pytest.mark.slow
class TestPerformance:
    """Performance tests (marked as slow)."""
    
    def test_decode_many_tracebacks(self):
        """Test decoding many tracebacks quickly."""
        for _ in range(100):
            for tb in SAMPLE_TRACEBACKS.values():
                result = decode_traceback(tb)
                assert result['success'] is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
