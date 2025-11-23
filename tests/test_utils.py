"""
Utility Functions Tests for pyDecode

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pytest
from pydecode.utils import (
    extract_error_type,
    extract_error_message,
    extract_line_number,
    extract_file_name,
    extract_function_name,
    sanitize_traceback,
    is_syntax_error,
    categorize_error,
    add_branding_footer,
    truncate_long_message,
    format_code_snippet
)
from tests import SAMPLE_TRACEBACKS


class TestExtractErrorType:
    """Tests for extract_error_type() function."""
    
    def test_extract_valueerror(self):
        tb = SAMPLE_TRACEBACKS['ValueError']
        assert extract_error_type(tb) == 'ValueError'
    
    def test_extract_zerodivisionerror(self):
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        assert extract_error_type(tb) == 'ZeroDivisionError'
    
    def test_extract_indexerror(self):
        tb = SAMPLE_TRACEBACKS['IndexError']
        assert extract_error_type(tb) == 'IndexError'
    
    def test_extract_keyerror(self):
        tb = SAMPLE_TRACEBACKS['KeyError']
        assert extract_error_type(tb) == 'KeyError'
    
    def test_extract_nameerror(self):
        tb = SAMPLE_TRACEBACKS['NameError']
        assert extract_error_type(tb) == 'NameError'
    
    def test_extract_typeerror(self):
        tb = SAMPLE_TRACEBACKS['TypeError']
        assert extract_error_type(tb) == 'TypeError'
    
    def test_extract_syntaxerror(self):
        tb = SAMPLE_TRACEBACKS['SyntaxError']
        assert extract_error_type(tb) == 'SyntaxError'
    
    def test_extract_empty_string(self):
        assert extract_error_type("") is None
    
    def test_extract_none_input(self):
        assert extract_error_type(None) is None


class TestExtractErrorMessage:
    """Tests for extract_error_message() function."""
    
    def test_extract_message_valueerror(self):
        tb = SAMPLE_TRACEBACKS['ValueError']
        msg = extract_error_message(tb)
        assert msg is not None
        assert "invalid literal" in msg.lower()
    
    def test_extract_message_zerodivision(self):
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        msg = extract_error_message(tb)
        assert msg is not None
        assert "division by zero" in msg.lower()
    
    def test_extract_message_keyerror(self):
        tb = SAMPLE_TRACEBACKS['KeyError']
        msg = extract_error_message(tb)
        assert msg is not None
        assert "missing_key" in msg


class TestExtractLineNumber:
    """Tests for extract_line_number() function."""
    
    def test_extract_line_valueerror(self):
        tb = SAMPLE_TRACEBACKS['ValueError']
        line_num = extract_line_number(tb)
        assert line_num is not None
        assert isinstance(line_num, int)
        assert line_num > 0
    
    def test_extract_line_zerodivision(self):
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        line_num = extract_line_number(tb)
        assert line_num is not None
        assert line_num == 10


class TestExtractFileName:
    """Tests for extract_file_name() function."""
    
    def test_extract_filename_valueerror(self):
        tb = SAMPLE_TRACEBACKS['ValueError']
        filename = extract_file_name(tb)
        assert filename is not None
        assert 'test.py' in filename
    
    def test_extract_filename_zerodivision(self):
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        filename = extract_file_name(tb)
        assert filename is not None
        assert 'calc.py' in filename


class TestExtractFunctionName:
    """Tests for extract_function_name() function."""
    
    def test_extract_function_zerodivision(self):
        tb = SAMPLE_TRACEBACKS['ZeroDivisionError']
        func_name = extract_function_name(tb)
        assert func_name is not None
        assert 'divide' in func_name


class TestSanitizeTraceback:
    """Tests for sanitize_traceback() function."""
    
    def test_sanitize_basic(self):
        tb = "  Line 1  \n  Line 2  \n"
        clean = sanitize_traceback(tb)
        assert clean == "Line 1  \n  Line 2"
    
    def test_sanitize_ansi_codes(self):
        tb = "\033[91mError\033[0m"
        clean = sanitize_traceback(tb)
        assert '\033' not in clean
        assert 'Error' in clean
    
    def test_sanitize_empty(self):
        assert sanitize_traceback("") == ""
        assert sanitize_traceback(None) == ""


class TestIsSyntaxError:
    """Tests for is_syntax_error() function."""
    
    def test_is_syntax_error_true(self):
        tb = SAMPLE_TRACEBACKS['SyntaxError']
        assert is_syntax_error(tb) is True
    
    def test_is_syntax_error_indentation(self):
        tb = SAMPLE_TRACEBACKS['IndentationError']
        assert is_syntax_error(tb) is True
    
    def test_is_syntax_error_false(self):
        tb = SAMPLE_TRACEBACKS['ValueError']
        assert is_syntax_error(tb) is False


class TestCategorizeError:
    """Tests for categorize_error() function."""
    
    def test_categorize_syntax(self):
        assert categorize_error('SyntaxError') == 'Syntax Errors'
    
    def test_categorize_name(self):
        assert categorize_error('NameError') == 'Name Errors'
    
    def test_categorize_type(self):
        assert categorize_error('TypeError') == 'Type Errors'
    
    def test_categorize_value(self):
        assert categorize_error('ValueError') == 'Value Errors'
    
    def test_categorize_arithmetic(self):
        assert categorize_error('ZeroDivisionError') == 'Arithmetic Errors'
    
    def test_categorize_unknown(self):
        assert categorize_error('UnknownError') == 'Other'


class TestAddBrandingFooter:
    """Tests for add_branding_footer() function."""
    
    def test_add_branding(self):
        text = "Some error message"
        result = add_branding_footer(text)
        assert "Powered by pyDecode" in result
        assert "Created by Yahya" in result
        assert "Some error message" in result


class TestTruncateLongMessage:
    """Tests for truncate_long_message() function."""
    
    def test_truncate_short_message(self):
        msg = "Short message"
        result = truncate_long_message(msg, 100)
        assert result == msg
    
    def test_truncate_long_message(self):
        msg = "A" * 300
        result = truncate_long_message(msg, 100)
        assert len(result) <= 100
        assert result.endswith("...")
    
    def test_truncate_none(self):
        result = truncate_long_message(None)
        assert result is None


class TestFormatCodeSnippet:
    """Tests for format_code_snippet() function."""
    
    def test_format_basic(self):
        code = "x = 1\ny = 2\nz = x / 0"
        result = format_code_snippet(code, 3, context_lines=1)
        assert "3 |" in result
        assert "Error here" in result
    
    def test_format_empty_code(self):
        result = format_code_snippet("", 1)
        assert result == ""


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
