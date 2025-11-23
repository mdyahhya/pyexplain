"""
PyExplain Test Suite

This package contains comprehensive tests for all PyExplain functionality.

Test Modules:
    - test_core.py: Tests for core decoding functions
    - test_mapping.py: Tests for exception mappings
    - test_utils.py: Tests for utility functions
    - test_cli.py: Tests for CLI functionality

Running Tests:
    pytest
    pytest --cov=pyexplain --cov-report=html
    pytest tests/test_core.py

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
TEST_DIR = Path(__file__).parent
PROJECT_ROOT = TEST_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test configuration
TEST_TIMEOUT = 30
SLOW_TEST_THRESHOLD = 5

# Sample tracebacks for testing
SAMPLE_TRACEBACKS = {
    "ValueError": """Traceback (most recent call last):
  File "test.py", line 5, in <module>
    x = int("abc")
ValueError: invalid literal for int() with base 10: 'abc'""",
    
    "ZeroDivisionError": """Traceback (most recent call last):
  File "calc.py", line 10, in divide
    result = a / b
ZeroDivisionError: division by zero""",
    
    "IndexError": """Traceback (most recent call last):
  File "list_test.py", line 3, in <module>
    item = my_list[10]
IndexError: list index out of range""",
    
    "KeyError": """Traceback (most recent call last):
  File "dict_test.py", line 4, in <module>
    value = my_dict['missing_key']
KeyError: 'missing_key'""",
    
    "NameError": """Traceback (most recent call last):
  File "script.py", line 7, in <module>
    print(undefined_variable)
NameError: name 'undefined_variable' is not defined""",
    
    "TypeError": """Traceback (most recent call last):
  File "type_test.py", line 2, in <module>
    result = "5" + 3
TypeError: can only concatenate str (not "int") to str""",
    
    "AttributeError": """Traceback (most recent call last):
  File "attr_test.py", line 3, in <module>
    x.nonexistent_method()
AttributeError: 'int' object has no attribute 'nonexistent_method'""",
    
    "SyntaxError": """  File "syntax_test.py", line 5
    if x == 5
            ^
SyntaxError: invalid syntax""",
    
    "IndentationError": """  File "indent_test.py", line 8
    return result
    ^
IndentationError: unexpected indent""",
}


def create_test_exception(exception_type: type, message: str = "test error"):
    """Create a test exception with a realistic traceback."""
    try:
        raise exception_type(message)
    except exception_type as e:
        return e


class TestHelper:
    """Helper class with utility methods for tests."""
    
    @staticmethod
    def assert_valid_decoded_output(result: dict):
        """Assert that a decoded result has all required fields."""
        required_fields = [
            'error_type',
            'simple_explanation',
            'fix_suggestion',
            'tags',
            'category',
            'emoji',
            'success'
        ]
        
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"
        
        assert isinstance(result['error_type'], str)
        assert isinstance(result['simple_explanation'], str)
        assert isinstance(result['fix_suggestion'], str)
        assert isinstance(result['tags'], list)
        assert isinstance(result['category'], str)
        assert isinstance(result['emoji'], str)
        assert isinstance(result['success'], bool)
        
        assert len(result['simple_explanation']) > 10, "Explanation too short"
        assert len(result['fix_suggestion']) > 10, "Fix suggestion too short"
        assert len(result['tags']) > 0, "No tags provided"
    
    @staticmethod
    def assert_contains_branding(text: str):
        """Assert that text contains PyExplain branding."""
        assert "Powered by PyExplain" in text or "Created by Yahya" in text
    
    @staticmethod
    def get_sample_traceback(error_type: str) -> str:
        """Get a sample traceback for testing."""
        return SAMPLE_TRACEBACKS.get(error_type, SAMPLE_TRACEBACKS['ValueError'])


__all__ = [
    'SAMPLE_TRACEBACKS',
    'create_test_exception',
    'TestHelper',
    'TEST_DIR',
    'PROJECT_ROOT',
    'TEST_TIMEOUT',
    'SLOW_TEST_THRESHOLD'
]
