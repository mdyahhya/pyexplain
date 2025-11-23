"""
pyDecode Command-Line Interface (CLI) Module

This module provides command-line tools for using pyDecode directly
from the terminal.

Commands:
    pydecode-run <file.py>    - Run a Python file and decode any errors
    pydecode --version        - Show version information
    pydecode --help           - Show help message

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, List

from pydecode.core import safe_run, format_decoded_output
from pydecode._version import (
    __version__,
    __title__,
    __description__,
    __author__,
    __company__,
    __branding__,
    print_version_info
)


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.
    
    Returns:
        Configured ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        prog='pydecode',
        description=f'{__title__} - {__description__}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Examples:
  pydecode script.py              Run script.py and decode any errors
  pydecode script.py --no-color   Run without colored output
  pydecode script.py --technical  Show technical error details
  pydecode --version              Show version information
  pydecode --help                 Show this help message

{__branding__}
Created by {__author__} | {__company__}
        '''
    )
    
    # Positional argument: file to run
    parser.add_argument(
        'file',
        type=str,
        nargs='?',
        help='Python file to execute and decode errors'
    )
    
    # Optional arguments
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Show version information and exit'
    )
    
    parser.add_argument(
        '-t', '--technical',
        action='store_true',
        help='Include technical error details in output'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    parser.add_argument(
        '--no-branding',
        action='store_true',
        help='Hide "Powered by pyDecode" branding footer'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Only show errors, suppress normal output'
    )
    
    parser.add_argument(
        '--raw',
        action='store_true',
        help='Show raw Python traceback instead of decoded version'
    )
    
    return parser


def run_file(file_path: str, technical: bool = False, color: bool = True,
            branding: bool = True, quiet: bool = False, raw: bool = False) -> int:
    """
    Run a Python file and decode any errors that occur.
    
    Args:
        file_path: Path to Python file to execute
        technical: Whether to show technical details
        color: Whether to use colored output
        branding: Whether to show branding footer
        quiet: Whether to suppress normal output
        raw: Whether to show raw traceback instead of decoded
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate file path
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ Error: File not found: {file_path}", file=sys.stderr)
        return 1
    
    if not path.is_file():
        print(f"❌ Error: Not a file: {file_path}", file=sys.stderr)
        return 1
    
    if not path.suffix == '.py':
        print(f"⚠️  Warning: {file_path} does not have .py extension", file=sys.stderr)
    
    # Read the file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        return 1
    
    # Run the code with safe_run
    if not quiet:
        print(f"🚀 Running {path.name}...\n")
    
    result = safe_run(code, filename=str(path), add_branding=branding)
    
    # Handle success
    if result.get('success'):
        if not quiet:
            print("✅ Code executed successfully!\n")
        
        # Print any output from the code
        output = result.get('output', '')
        if output:
            print("📤 Output:")
            print(output)
        
        # Show branding if enabled
        if branding and not quiet:
            print("─" * 72)
            print(f"{__branding__}\n")
        
        return 0
    
    # Handle error
    if raw:
        # Show raw traceback
        print(result.get('raw_traceback', 'No traceback available'))
    else:
        # Show decoded error
        formatted = format_decoded_output(result, include_technical=technical, color=color)
        print(formatted)
    
    # Print any output before the error
    output = result.get('output', '')
    if output and not quiet:
        print("\n📤 Output before error:")
        print(output)
    
    return 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        argv: Command-line arguments (default: sys.argv[1:])
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Handle --version flag
    if args.version:
        print_version_info()
        return 0
    
    # Require file argument if not showing version
    if not args.file:
        parser.print_help()
        return 1
    
    # Run the file
    return run_file(
        file_path=args.file,
        technical=args.technical,
        color=not args.no_color,
        branding=not args.no_branding,
        quiet=args.quiet,
        raw=args.raw
    )


def cli_entry_point():
    """
    Entry point for console script (used by setuptools).
    This is called when user runs 'pydecode' or 'pydecode-run' command.
    """
    sys.exit(main())


if __name__ == '__main__':
    # Allow running as: python -m pydecode.cli
    sys.exit(main())


# Public API
__all__ = [
    'main',
    'cli_entry_point',
    'run_file',
    'create_parser'
]
