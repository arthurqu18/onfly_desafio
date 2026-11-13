"""Testes unitários para a data de geração do relatório."""

from datetime import datetime, timezone, timedelta

from helpers import build_report


def test_report_uses_supplied_generation_time(tmp_path):
    """A data fornecida ao construtor aparece no formato ISO esperado."""
    generated_at = datetime(2025, 6, 15, 14, 30, 45, tzinfo=timezone(timedelta(hours=-3)))

    report = build_report(tmp_path, [], now=generated_at)

    assert report["generated_at"] == "2025-06-15T14:30:45-03:00"
