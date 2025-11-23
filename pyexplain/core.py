"""
PyExplain Core Module

Main decoding logic for converting Python errors into beginner-friendly explanations.

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import sys
import traceback as tb_module
from typing import Dict, Optional, Any
from io import StringIO
import contextlib

from pyexplain.mapping import get_exception_mapping
from pyexplain.utils import (
    extract_error_type,
    extract_error_message,
    extract_line_number,
    extract_file_name,
    extract_function_name,
    sanitize_traceback,
    format_exception_from_object,
    categorize_error,
    truncate_long_message,
    is_syntax_error,
    parse_syntax_error_details
)
from pyexplain._version import __branding__, __version__


def decode_traceback(traceback_text: str, add_branding: bool = True) -> Dict[str, Any]:
    """Decode a raw Python traceback string into a beginner-friendly explanation."""
    if not traceback_text or not isinstance(traceback_text, str):
        return {
            "error_type": "InvalidInput",
            "original_message": "No traceback provided",
            "simple_explanation": "PyExplain needs a valid error traceback to decode.",
            "fix_suggestion": "Make sure you're passing a Python error message to decode_traceback().",
            "line_number": None,
            "file_name": None,
            "function_name": None,
            "tags": ["invalid_input"],
            "category": "Input Error",
            "emoji": "⚠️",
            "branding": __branding__ if add_branding else None,
            "success": False,
            "raw_traceback": ""
        }
    
    clean_traceback = sanitize_traceback(traceback_text)
    error_type = extract_error_type(clean_traceback)
    error_message = extract_error_message(clean_traceback)
    line_number = extract_line_number(clean_traceback)
    file_name = extract_file_name(clean_traceback)
    function_name = extract_function_name(clean_traceback)
    mapping = get_exception_mapping(error_type or "__unknown__")
    
    result = {
        "error_type": error_type or "UnknownError",
        "original_message": truncate_long_message(error_message or "No message provided"),
        "simple_explanation": mapping["simple_explanation"],
        "fix_suggestion": mapping["fix_suggestion"],
        "line_number": line_number,
        "file_name": file_name,
        "function_name": function_name,
        "tags": mapping["tags"],
        "category": categorize_error(error_type),
        "emoji": mapping["emoji"],
        "branding": __branding__ if add_branding else None,
        "success": False,
        "raw_traceback": clean_traceback
    }
    
    if is_syntax_error(clean_traceback):
        result["syntax_details"] = parse_syntax_error_details(clean_traceback)
    
    return result


def decode_exception(exception: Exception, add_branding: bool = True) -> Dict[str, Any]:
    """Decode an Exception object directly into a beginner-friendly explanation."""
    if not isinstance(exception, BaseException):
        return {
            "error_type": "InvalidInput",
            "original_message": "Not a valid exception object",
            "simple_explanation": "PyExplain needs a valid Exception object.",
            "fix_suggestion": "Use decode_exception() only with exception objects from except blocks.",
            "line_number": None,
            "file_name": None,
            "function_name": None,
            "tags": ["invalid_input"],
            "category": "Input Error",
            "emoji": "⚠️",
            "branding": __branding__ if add_branding else None,
            "success": False,
            "raw_traceback": ""
        }
    
    traceback_text = format_exception_from_object(exception)
    return decode_traceback(traceback_text, add_branding=add_branding)


def safe_run(code: str, filename: str = "<string>", globals_dict: Optional[dict] = None,
             locals_dict: Optional[dict] = None, add_branding: bool = True) -> Dict[str, Any]:
    """Safely execute Python code and automatically decode any errors."""
    if not code or not isinstance(code, str):
        return {
            "success": False,
            "error_type": "InvalidInput",
            "original_message": "No code provided",
            "simple_explanation": "PyExplain needs valid Python code to run.",
            "fix_suggestion": "Pass a string containing Python code to safe_run().",
            "line_number": None,
            "file_name": None,
            "function_name": None,
            "tags": ["invalid_input"],
            "category": "Input Error",
            "emoji": "⚠️",
            "branding": __branding__ if add_branding else None,
            "output": "",
            "raw_traceback": ""
        }
    
    if globals_dict is None:
        globals_dict = {"__name__": "__main__", "__file__": filename}
    if locals_dict is None:
        locals_dict = globals_dict
    
    stdout_capture = StringIO()
    
    try:
        with contextlib.redirect_stdout(stdout_capture):
            compiled_code = compile(code, filename, 'exec')
            exec(compiled_code, globals_dict, locals_dict)
        
        return {
            "success": True,
            "output": stdout_capture.getvalue(),
            "result": locals_dict.get('result', None),
            "branding": __branding__ if add_branding else None,
            "message": "Code executed successfully! ✅"
        }
        
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_text = ''.join(tb_module.format_exception(exc_type, exc_value, exc_traceback))
        decoded = decode_traceback(traceback_text, add_branding=add_branding)
        decoded["output"] = stdout_capture.getvalue()
        return decoded


def format_decoded_output(decoded: Dict[str, Any], include_technical: bool = False,
                         color: bool = False) -> str:
    """Format a decoded error dictionary into a human-readable string."""
    if not decoded or not isinstance(decoded, dict):
        return "Invalid decoded data"
    
    RED = '\033[91m' if color else ''
    GREEN = '\033[92m' if color else ''
    YELLOW = '\033[93m' if color else ''
    CYAN = '\033[96m' if color else ''
    MAGENTA = '\033[95m' if color else ''
    BLUE = '\033[94m' if color else ''
    RESET = '\033[0m' if color else ''
    BOLD = '\033[1m' if color else ''
    
    lines = []
    error_type = decoded.get('error_type', 'Error')
    emoji = decoded.get('emoji', '⚠️')
    
    lines.append("")
    lines.append("╔" + "═" * 70 + "╗")
    lines.append(f"║  {BOLD}{RED}{emoji} {error_type}{RESET}" + " " * (68 - len(error_type) - 2) + "║")
    lines.append("╚" + "═" * 70 + "╝")
    lines.append("")
    lines.append(f"{BOLD}{CYAN}💡 Simple Explanation:{RESET}")
    lines.append(decoded.get('simple_explanation', 'No explanation available'))
    lines.append("")
    lines.append(f"{BOLD}{GREEN}🔧 How to Fix:{RESET}")
    lines.append(decoded.get('fix_suggestion', 'No suggestion available'))
    lines.append("")
    
    if decoded.get('file_name') or decoded.get('line_number'):
        lines.append(f"{BOLD}{YELLOW}📍 Error Location:{RESET}")
        if decoded.get('file_name'):
            lines.append(f"   File: {decoded['file_name']}")
        if decoded.get('line_number'):
            lines.append(f"   Line: {decoded['line_number']}")
        if decoded.get('function_name'):
            lines.append(f"   Function: {decoded['function_name']}")
        lines.append("")
    
    if include_technical:
        lines.append(f"{BOLD}{MAGENTA}🔍 Technical Details:{RESET}")
        lines.append(f"   Category: {decoded.get('category', 'Unknown')}")
        lines.append(f"   Original Message: {decoded.get('original_message', 'N/A')}")
        lines.append(f"   Tags: {', '.join(decoded.get('tags', []))}")
        lines.append("")
    
    if decoded.get('branding'):
        lines.append("─" * 72)
        lines.append(f"{BOLD}{BLUE}{decoded['branding']}{RESET}")
        lines.append("")
    
    return '\n'.join(lines)


__all__ = ['decode_traceback', 'decode_exception', 'safe_run', 'format_decoded_output']
