"""Testes unitários para relatórios sem reservas."""

from helpers import build_report


def test_empty_reservations_produce_zero_summary(tmp_path):
    """Um CSV sem linhas gera totais zerados e coleções vazias."""
    report = build_report(tmp_path, [])

    assert report["summary"] == {
        "total_reservations": 0,
        "confirmed_reservations": 0,
        "cancelled_reservations": 0,
        "no_show_reservations": 0,
        "total_room_nights": 0,
        "total_amount_brl": "0.00",
        "average_nightly_rate_brl": "0.00",
    }
    assert report["by_month"] == []
    assert report["top_hotels"] == []
