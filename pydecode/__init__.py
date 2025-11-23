"""
pyDecode - Convert Python Errors into Beginner-Friendly Explanations

pyDecode is a Python library that takes raw Python error tracebacks and
converts them into simple, easy-to-understand explanations with helpful
fix suggestions. Perfect for beginners learning Python!

Quick Start:
    >>> import pydecode
    >>> 
    >>> # Decode a traceback string
    >>> traceback_text = "ValueError: invalid literal for int()"
    >>> result = pydecode.decode_traceback(traceback_text)
    >>> print(result['simple_explanation'])
    >>> 
    >>> # Decode an exception directly
    >>> try:
    ...     x = int("abc")
    ... except Exception as e:
    ...     result = pydecode.decode_exception(e)
    ...     print(result['fix_suggestion'])
    >>> 
    >>> # Run code safely and auto-decode errors
    >>> code = "print(10 / 0)"
    >>> result = pydecode.safe_run(code)
    >>> if not result['success']:
    ...     print(result['simple_explanation'])

Main Functions:
    - decode_traceback(traceback_text: str) -> dict
    - decode_exception(exception: Exception) -> dict
    - safe_run(code: str, filename: str = "<string>") -> dict
    - format_decoded_output(decoded: dict) -> str

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
Website: https://dominal.in
License: MIT

GitHub: https://github.com/mdyahhya/pydecode
PyPI: https://pypi.org/project/pydecode/
"""

# Version information
from pydecode._version import (
    __version__,
    __version_info__,
    __title__,
    __description__,
    __url__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
    __company__,
    __company_url__,
    __branding__,
    __python_requires__,
    __python_versions__,
    __status__,
    __release_date__,
    __api_version__,
    get_version,
    get_version_info,
    print_version_info
)

# Core functionality
from pydecode.core import (
    decode_traceback,
    decode_exception,
    safe_run,
    format_decoded_output
)

# Utilities (advanced users)
from pydecode.utils import (
    extract_error_type,
    extract_error_message,
    extract_line_number,
    extract_file_name,
    extract_function_name,
    sanitize_traceback,
    categorize_error
)

# Mapping access (for customization)
from pydecode.mapping import (
    EXCEPTION_MAPPINGS,
    get_exception_mapping
)

# Internationalization
from pydecode.i18n import (
    translate,
    supported_languages
)


# Define public API (what gets imported with "from pydecode import *")
__all__ = [
    # Version info
    '__version__',
    '__version_info__',
    '__title__',
    '__description__',
    '__url__',
    '__author__',
    '__author_email__',
    '__license__',
    '__copyright__',
    '__company__',
    '__company_url__',
    '__branding__',
    '__python_requires__',
    '__python_versions__',
    '__status__',
    '__release_date__',
    '__api_version__',
    'get_version',
    'get_version_info',
    'print_version_info',
    
    # Core functions (PRIMARY API)
    'decode_traceback',
    'decode_exception',
    'safe_run',
    'format_decoded_output',
    
    # Utilities (SECONDARY API)
    'extract_error_type',
    'extract_error_message',
    'extract_line_number',
    'extract_file_name',
    'extract_function_name',
    'sanitize_traceback',
    'categorize_error',
    
    # Mapping (ADVANCED API)
    'EXCEPTION_MAPPINGS',
    'get_exception_mapping',
    
    # i18n (EXPERIMENTAL API)
    'translate',
    'supported_languages'
]


# Package-level convenience function
def decode(input_data, **kwargs):
    """
    Smart decode function that accepts either a traceback string or Exception object.
    
    This is a convenience wrapper that automatically detects the input type
    and calls the appropriate decode function.
    
    Args:
        input_data: Either a traceback string or an Exception object
        **kwargs: Additional arguments passed to decode_traceback or decode_exception
        
    Returns:
        Decoded error dictionary
        
    Example:
        >>> # Works with both strings and exceptions
        >>> result = pydecode.decode("ValueError: bad value")
        >>> result = pydecode.decode(ValueError("bad value"))
    """
    if isinstance(input_data, BaseException):
        return decode_exception(input_data, **kwargs)
    elif isinstance(input_data, str):
        return decode_traceback(input_data, **kwargs)
    else:
        raise TypeError(
            f"decode() expects a string or Exception, got {type(input_data).__name__}"
        )


# Add decode to public API
__all__.append('decode')


# Package initialization message (optional, can be removed if too verbose)
def _show_welcome_message():
    """
    Show a welcome message when package is first imported (development only).
    This is disabled by default for production use.
    """
    import os
    if os.getenv('PYDECODE_WELCOME', '').lower() in ('1', 'true', 'yes'):
        print(f"✨ {__title__} v{__version__} loaded successfully!")
        print(f"   {__branding__}")
        print(f"   Use pydecode.decode_traceback() to get started!")
        print()


# Uncomment to enable welcome message (for development/debugging)
# _show_welcome_message()


# Type hints support (PEP 561)
# This tells type checkers that this package includes type hints
__all__.append('py.typed')
