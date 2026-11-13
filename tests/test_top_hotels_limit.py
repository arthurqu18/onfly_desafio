"""Testes unitários para o limite do ranking de hotéis."""

from helpers import build_report


def test_top_hotels_respect_requested_limit(tmp_path):
    """O ranking retorna somente a quantidade de hotéis solicitada."""
    report = build_report(
        tmp_path,
        [
            {"hotel_id": "H01", "hotel_name": "Hotel A", "amount": "300.00"},
            {"hotel_id": "H02", "hotel_name": "Hotel B", "amount": "200.00"},
            {"hotel_id": "H03", "hotel_name": "Hotel C", "amount": "100.00"},
        ],
        top=2,
    )

    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02"]
