"""A collection of utility functions for managing csv-file-related actions."""

from pathlib import Path, PurePath
from textwrap import dedent
import sys
import csv
import re

# The maximum number of lines in the csv file within which valid column headers must exist
MAX_CSV_ROWS_TO_FIND_HEADERS = 6


def get_csv_absolute_path(film_csv_path: str) -> str:
    """Gets and returns the user-entered absolute path of the csv file.

    If no absolute path is given, the user is repeatedly prompted.
    """
    # only absolute paths are accepted
    while not PurePath.is_absolute(PurePath(film_csv_path)):
        short_message = 'The path you provided is not a full path.'
        film_csv_path = get_csv_path(short_message)

    # the file must exist
    while not Path.exists(Path(film_csv_path)):
        short_message = 'The file you provided does not exist.'
        film_csv_path = get_csv_path(short_message)

    # the existing file must be a .csv file
    while '.csv' not in PurePath(film_csv_path).suffix:
        short_message = 'The file you provided is not a .csv file.'
        film_csv_path = get_csv_path(short_message)

    return film_csv_path


def get_csv_path(short_message: str) -> str:
    """Gets, and returns the user-entered csv path.

    The message displayed while asking for input is a combination of the provided short message,
    and a message that asks for an absolute path to be entered.
    """
    full_message = dedent(
        f"""
        {short_message}
        Please re-enter the full path again.
        (q to quit)
        full path > """
    )
    try:
        film_csv_path = input(full_message)
    except KeyboardInterrupt:
        sys.exit('\nGoodbye')
    else:
        if film_csv_path.lower() == 'q':
            sys.exit('Goodbye!')
    return film_csv_path


def is_valid_letterboxd_format(csv_file: str, max_lines_to_check=MAX_CSV_ROWS_TO_FIND_HEADERS) -> bool:
    """Checks whether the provided csv list of films has column headers compatible with
    Letterboxd's csv format.

    The provided file must include at least the two columns `URL`(or `LetterboxdURI`) and `Name`.
    The `URL` points to the film's page on `https://letterboxd.com/`, and
    The `Name` is the name/title of the film.
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        line_count = 0
        reader = csv.reader(f)

        for line in reader:
            if line_count == max_lines_to_check:
                return False

            rows = ', '.join(line)
            # Name and URL column headers can be in any order
            if match := re.search(r'(Name,).*(URL)|(URL,).*(Name)', rows):
                return True
            line_count += 1
    return True


def valid_csv_format_message() -> str:
    """Returns information about expected format for the movie list csv file."""
    message = dedent(
        f"""
    Could not find either or both of the column labels `Name` and `URL`.
    
    Make sure those column labels occur within the first {MAX_CSV_ROWS_TO_FIND_HEADERS} lines of your
    csv file.
    
    The expected format looks similar to this 
    (`Name` and `URL` columns can be in any order):

    │ ... │ ...    │ ... │ ...                  │ ... │
    ├─────┼────────┼─────┼──────────────────────┼─────┤
    │ ... │ Name   │ ... │ URL                  │ ... │
    ├─────┼────────┼─────┼──────────────────────┼─────┤
    │ ... │ Amélie │ ... │ https://boxd.it/2aUc │ ... │
    ├─────┼────────┼─────┼──────────────────────┼─────┤
    │ ... │ RRR    │ ... │ https://boxd.it/ljDs │ ... │
    ├─────┼────────┼─────┼──────────────────────┼─────┤
    │ ... │ Oldboy │ ... │ https://boxd.it/29R2 │ ... │
    ├─────┼────────┼─────┼──────────────────────┼─────┤
    │ ... │ ...    │ ... │ ...                  │ ... │
    
    Check your csv file and try again.
    """
    )

    return message
