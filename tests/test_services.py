from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from barbersync import services

PANAMA = ZoneInfo(services.TIMEZONE)
UTC = ZoneInfo("UTC")


@pytest.mark.parametrize(
    "phone,expected",
    [
        ("6000-0000", "+50760000000"),
        ("60000000", "+50760000000"),
        ("+507 6000-0000", "+50760000000"),
        ("50760000000", "+50760000000"),
    ],
)
def test_normalize_phone(phone, expected):
    assert services.normalize_phone(phone) == expected


def test_normalize_phone_invalid():
    with pytest.raises(ValueError):
        services.normalize_phone("123")


def test_panama_to_utc():
    panama = datetime(2026, 11, 20, 10, 0, tzinfo=PANAMA)
    utc = services.panama_to_utc(panama)
    assert utc.hour == 15
    assert utc.tzinfo == UTC


def test_utc_to_panama_str():
    text = "2026-11-20T15:00:00Z"
    panama = services.utc_to_panama_str(text)
    assert "-05:00" in panama
    assert "10:00" in panama


def test_utc_to_panama_str_naive():
    text = "2026-11-20T15:00:00"
    panama = services.utc_to_panama_str(text)
    assert "-05:00" in panama
