"""Testes unitários para reservas com múltiplos quartos."""

from helpers import build_report


def test_room_nights_and_average_include_all_rooms(tmp_path):
    """O total de noites considera quartos e a média usa esse total."""
    report = build_report(
        tmp_path,
        [
            {
                "checkin_date": "2025-03-10",
                "checkout_date": "2025-03-13",
                "rooms": "2",
                "amount": "600.00",
            }
        ],
    )

    assert report["summary"]["total_room_nights"] == 6
    assert report["summary"]["total_amount_brl"] == "600.00"
    assert report["summary"]["average_nightly_rate_brl"] == "100.00"
