"""Testes unitários para entradas inválidas de reservas."""

import pytest

from helpers import build_report
from onfly_report.exceptions import InputFileError


def test_invalid_checkin_date_is_reported_as_input_error(tmp_path):
    """Uma data inválida interrompe a construção com erro de entrada."""
    with pytest.raises(InputFileError, match="linha 2 inválida"):
        build_report(tmp_path, [{"checkin_date": "not-a-date"}])
