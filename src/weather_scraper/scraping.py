"""Provides scraping methods for wowt.com."""
from dataclasses import dataclass
from typing import List
from typing import Optional

import pendulum
import requests
from bs4 import BeautifulSoup
from lxml import etree
from pendulum.datetime import DateTime
from requests.models import Response


@dataclass
class SiteConfig:
    """Dataclass for storing site configurations."""

    name: str
    url: str


sites = {"wowt": SiteConfig(name="url", url="https://www.wowt.com/weather")}


def scrape(site_name: str) -> Optional[Response]:
    """Provides basic scraping of sites using site configurations.

    Args:
        site_name (str): The name of site to scrape.

    Returns:
        Optional[Response]: Returns a Response object or None.
    """
    site = sites.get(site_name)
    if site is not None:
        resp = requests.get(site.url)
        return resp


def parse_wowt_hourly(response_text: str, recorded_time: DateTime) -> List:
    """Parses hourly forecast data from wowt website source.

    Args:
        response_text (str): HTML source from wowt website.
        recorded_time (DateTime): DateTime for when source was captured.

    Returns:
        List: List of hourly forecast data in dictionary format.
    """
    soup = BeautifulSoup(response_text, "html.parser")
    dom = etree.HTML(text=str(soup), parser=None)

    timezone = "America/Chicago"
    year = recorded_time.year
    hourly_forecasts = []
    for index in range(2, 14):
        hour_string = dom.xpath(
            f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div[1]/div[{index}]/div[1]/span[1]'
        )[0].text
        month_day = dom.xpath(
            f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div[1]/div[{index}]/div[1]/span[2]'
        )[0].text
        dt_string = f"{month_day}/{year} {hour_string}"
        dt = pendulum.from_format(dt_string, "M/D/YYYY h A", tz=timezone)
        valid_timestamp = dt.timestamp()
        temperature = int(
            dom.xpath(
                f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div[1]/div[{index}]/div[2]/text()[1]'
            )[0]
        )
        precip_chance = int(
            dom.xpath(
                f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div[1]/div[{index}]/div[4]/text()[1]'
            )[0]
        )
        hourly_forecasts.append(
            {
                "valid_time": valid_timestamp,
                "recorded_time": recorded_time.timestamp(),
                "temperature": temperature,
                "precip_chance": precip_chance,
            }
        )
    return hourly_forecasts


def parse_wowt_ten_day(page_content: str, recorded_time: DateTime) -> List:
    """Parses 10-day forecast data from wowt website source content.

    Args:
        page_content (str): HTML source from wowt with 10-day forecast.
        recorded_time (DateTime): DateTime for when page content was recorded.

    Returns:
        List: A list of dictionaries containing 10-day forecast details.
    """
    soup = BeautifulSoup(page_content, "html.parser")
    dom = etree.HTML(str(soup), parser=None)

    year = recorded_time.year
    ten_day_forecasts = []

    for index in range(2, 12):
        month_day = dom.xpath(
            f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div/div[{index}]/div[1]/span[3]'
        )[0].text
        dt_string = f"{month_day}/{year}"
        dt = pendulum.from_format(dt_string, "M/D/YYYY", tz="America/Chicago")
        valid_date = dt.date().isoformat()
        high_temp = int(
            dom.xpath(
                f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div/div[{index}]/div[2]/div/span[1]'
            )[0].text.rstrip("°")
            or -99
        )
        low_temp = int(
            dom.xpath(
                f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div/div[{index}]/div[2]/span/text()[1]'
            )[0].rstrip("°")
        )
        precip_chance = int(
            dom.xpath(
                f'//*[@id="homepage-layout"]/div/div/div[1]/section[1]/div[2]/div/div[2]/div/div[{index}]/div[4]/text()[1]'
            )[0].rstrip("%")
        )
        ten_day_forecasts.append(
            {
                "valid_date": valid_date,
                "recorded_time": recorded_time.timestamp(),
                "high_temp": high_temp,
                "low_temp": low_temp,
                "precip_chance": precip_chance,
            }
        )
    return ten_day_forecasts
