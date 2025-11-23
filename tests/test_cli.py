"""
CLI Tests for PyExplain

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

import pytest
from pyexplain.cli import main, create_parser


class TestCLIParser:
    """Tests for CLI argument parser."""
    
    def test_parser_creation(self):
        parser = create_parser()
        assert parser is not None
    
    def test_parser_version_flag(self):
        parser = create_parser()
        args = parser.parse_args(['--version'])
        assert args.version is True


class TestCLIMain:
    """Tests for CLI main function."""
    
    def test_main_with_version(self, capsys):
        exit_code = main(['--version'])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert 'PyExplain' in captured.out or 'PyExplain' in str(captured)
    
    def test_main_no_args(self):
        exit_code = main([])
        assert exit_code == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
