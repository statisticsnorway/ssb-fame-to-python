"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Fame To Python."""


if __name__ == "__main__":
    main(prog_name="ssb-fame-to-python")  # pragma: no cover
