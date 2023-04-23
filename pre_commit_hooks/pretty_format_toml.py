"""A pre-commit script that formats a TOML file with taplo."""

import re
from subprocess import run
from typing import Iterable

import click


@click.command
@click.argument("files", nargs=-1)
@click.option(
    "--autofix/--no-autofix",
    default=False,
    help="Whether to automatically format files that aren't properly formatted.",
)
def main(files: Iterable[str], autofix: bool) -> None:
    """Format a TOML file with taplo.

    This script assumes that taplo is in your path.

    This will check and format all of the files in FILES.
    """
    log_line_regex = re.compile(r'''path="?P<toml_path>.+"''')
    check_command = ["taplo", "format", "--check"] + list(files)
    # Regardless of whether we are going to actually format the files, we want
    # to run an check first so we can report which files aren't formatted
    # properly.
    check_result = run(check_command, capture_output=True, text=True)
    badly_formatted_files = []
    if check_result.returncode != 0:
        for log_line in check_result.stderr:
            search_result = log_line_regex.search(log_line)
            if search_result is None:
                continue
            toml_path = search_result["toml_path"]
            badly_formatted_files.append(toml_path)

    if autofix:
        format_command = ["taplo", "format"] + list(files)
        run(format_command, check=True)
        print("The following files were formatted with taplo: " +
              "\n- ".join(badly_formatted_files))
    else:
        print("The following files are not correctly formatted: " +
              "\n- ".join(badly_formatted_files))


if __name__ == "__main__":
    main()  # type: ignore
