from subprocess import run
from typing import Iterable

import click


@click.command
@click.argument("files", nargs=-1)
def main(files: Iterable[str]) -> None:
    """Validate a TOML file's schema with taplo.

    This script assumes that taplo is in your path.

    This will check all of the files provided in FILES.
    """
    check_command = ["taplo", "lint"] + list(files)
    run(check_command, check=True)


if __name__ == "__main__":
    main()  # type: ignore
