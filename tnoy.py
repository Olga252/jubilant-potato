import pytest
from unittest.mock import patch
from io import StringIO
from  tras import main


def test_invalid_choice():
    user_input = "6\n1\n5\n"
    with patch('builtins.input', side_effect=user_input.splitlines()), \
            patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        main()

        output = mock_stdout.getvalue()
        assert "Некорректный ввод. Пожалуйста, введите число от 1 до 5." in output
