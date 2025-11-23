"""
CLI Tests for pyDecode

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pytest
import sys
from pathlib import Path
from io import StringIO
from pydecode.cli import main, create_parser, run_file


class TestCLIParser:
    """Tests for CLI argument parser."""
    
    def test_parser_creation(self):
        parser = create_parser()
        assert parser is not None
    
    def test_parser_version_flag(self):
        parser = create_parser()
        args = parser.parse_args(['--version'])
        assert args.version is True
    
    def test_parser_help_flag(self):
        parser = create_parser()
        args = parser.parse_args(['--help'])
        # Help will exit, so just test it parses


class TestCLIMain:
    """Tests for CLI main function."""
    
    def test_main_with_version(self, capsys):
        exit_code = main(['--version'])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'pyDecode' in captured.out or 'pyDecode' in str(captured)
    
    def test_main_no_args(self):
        exit_code = main([])
        assert exit_code == 1  # Should fail without file argument


class TestCLIRunFile:
    """Tests for run_file function."""
    
    def test_run_nonexistent_file(self, capsys):
        exit_code = run_file('nonexistent_file.py')
        assert exit_code == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
