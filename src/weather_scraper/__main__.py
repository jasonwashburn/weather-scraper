"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Weather Scraper."""


if __name__ == "__main__":
    main(prog_name="weather-scraper")  # pragma: no cover
