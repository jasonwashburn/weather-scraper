"""Tests for scraping module."""

import pendulum
import pytest

from weather_scraper.scraping import parse_wowt_hourly
from weather_scraper.scraping import parse_wowt_ten_day
from weather_scraper.scraping import scrape


@pytest.fixture
def wowt_hourly_response() -> str:
    """Testing fixture for canned response from wowt website with hourly data.

    Returns:
        str: HTML source for wowt website with hourly data.
    """
    with open("tests/wowt_hourly_fixture.txt") as f:
        return f.read()


@pytest.fixture
def wowt_ten_day_content() -> str:
    """Testing fixture for canned response from wowt website with 10-day data.

    Returns:
        str: HTML source for wowt website with 10-day data.
    """
    with open("tests/wowt_10day_fixture.txt") as f:
        return f.read()


def test_scrape_returns_status_ok():
    """Tests wowt url returns status code 200 and html document."""
    result = scrape(site_name="wowt")
    if result is not None:
        assert result.status_code == 200
        assert result.text[:15] == "<!DOCTYPE html>"
    else:
        raise AssertionError("Result returned None")


def test_parse_wowt_hourly(wowt_hourly_response: str):
    """Tests proper parsing of wowt hourly data.

    Args:
        wowt_hourly_response (str): html source for wowt hourly data.
    """
    recorded_time = pendulum.datetime(
        year=2022, month=1, day=1, hour=1, tz="America/Chicago"
    )
    result = parse_wowt_hourly(
        response_text=wowt_hourly_response, recorded_time=recorded_time
    )
    expected_result = [
        {
            "valid_time": 1657486800.0,
            "recorded_time": 1641020400.0,
            "temperature": 92,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657490400.0,
            "recorded_time": 1641020400.0,
            "temperature": 92,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657494000.0,
            "recorded_time": 1641020400.0,
            "temperature": 91,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657497600.0,
            "recorded_time": 1641020400.0,
            "temperature": 90,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657501200.0,
            "recorded_time": 1641020400.0,
            "temperature": 89,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657504800.0,
            "recorded_time": 1641020400.0,
            "temperature": 86,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657508400.0,
            "recorded_time": 1641020400.0,
            "temperature": 84,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657512000.0,
            "recorded_time": 1641020400.0,
            "temperature": 82,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657515600.0,
            "recorded_time": 1641020400.0,
            "temperature": 80,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657519200.0,
            "recorded_time": 1641020400.0,
            "temperature": 79,
            "precip_chance": 0,
        },
        {
            "valid_time": 1657522800.0,
            "recorded_time": 1641020400.0,
            "temperature": 78,
            "precip_chance": 20,
        },
        {
            "valid_time": 1657526400.0,
            "recorded_time": 1641020400.0,
            "temperature": 77,
            "precip_chance": 30,
        },
    ]
    assert result == expected_result


def test_parse_wowt_ten_day(wowt_ten_day_content: str):
    """Tests proper parsing of wowt 10-day data.

    Args:
        wowt_ten_day_content (str): html source for wowt 10-day data.
    """
    recorded_time = pendulum.datetime(
        year=2022, month=1, day=1, hour=1, tz="America/Chicago"
    )
    result = parse_wowt_ten_day(
        page_content=wowt_ten_day_content, recorded_time=recorded_time
    )
    expected_result = [
        {
            "valid_date": "2022-07-10",
            "recorded_time": 1641020400.0,
            "high_temp": -99,
            "low_temp": 71,
            "precip_chance": 60,
        },
        {
            "valid_date": "2022-07-11",
            "recorded_time": 1641020400.0,
            "high_temp": 86,
            "low_temp": 62,
            "precip_chance": 30,
        },
        {
            "valid_date": "2022-07-12",
            "recorded_time": 1641020400.0,
            "high_temp": 87,
            "low_temp": 64,
            "precip_chance": 0,
        },
        {
            "valid_date": "2022-07-13",
            "recorded_time": 1641020400.0,
            "high_temp": 90,
            "low_temp": 68,
            "precip_chance": 0,
        },
        {
            "valid_date": "2022-07-14",
            "recorded_time": 1641020400.0,
            "high_temp": 92,
            "low_temp": 72,
            "precip_chance": 0,
        },
        {
            "valid_date": "2022-07-15",
            "recorded_time": 1641020400.0,
            "high_temp": 95,
            "low_temp": 73,
            "precip_chance": 0,
        },
        {
            "valid_date": "2022-07-16",
            "recorded_time": 1641020400.0,
            "high_temp": 95,
            "low_temp": 72,
            "precip_chance": 20,
        },
        {
            "valid_date": "2022-07-17",
            "recorded_time": 1641020400.0,
            "high_temp": 94,
            "low_temp": 72,
            "precip_chance": 0,
        },
        {
            "valid_date": "2022-07-18",
            "recorded_time": 1641020400.0,
            "high_temp": 94,
            "low_temp": 74,
            "precip_chance": 0,
        },
        {
            "valid_date": "2022-07-19",
            "recorded_time": 1641020400.0,
            "high_temp": 96,
            "low_temp": 75,
            "precip_chance": 0,
        },
    ]
    assert result == expected_result
