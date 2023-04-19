"""A collection of utility functions for managing csv-file-related actions."""

from pathlib import Path, PurePath
from textwrap import dedent
import sys
import csv
import re
from collections import namedtuple

MAX_CSV_ROWS_TO_FIND_HEADERS = 6

# all possible orders of the `URL`, `Name`, and `year` columns in the csv file
CSV_REQUIRED_HEADERS_PATTERN = r"""
(URL).*(Name).*(Year)|
(URL).*(Year).*(Name)|
(Name).*(URL).*(Year)|
(Name).*(Year).*(URL)|
(Year).*(URL).*(Name)|
(Year).*(Name).*(URL)
""".strip()

CSVInfo = namedtuple('CSVInfo', ['extra_info', 'headers', 'header_info'])


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


def is_valid_letterboxd_format(
    csv_file: str, max_lines_to_check=MAX_CSV_ROWS_TO_FIND_HEADERS, header_pattern=CSV_REQUIRED_HEADERS_PATTERN
) -> bool:
    """Checks whether the provided csv list of films has column headers compatible with
    Letterboxd's csv format.

    The provided file must include at least the three columns `URL`(or `LetterboxdURI`), `Name`, and `Year`.

    The `URL` points to the film's page on `https://letterboxd.com/`,

    The `Name` is the name/title of the film, and

    The `Year` is the year of release of the film.
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        line_count = 0
        reader = csv.reader(f)

        for line in reader:
            if line_count == max_lines_to_check:
                return False

            rows = ', '.join(line)
            # Name and URL column headers can be in any order
            if re.search(header_pattern, rows, re.VERBOSE):
                return True
            line_count += 1
    return True


def get_csv_sections(csv_file: str, header_pattern=CSV_REQUIRED_HEADERS_PATTERN) -> CSVInfo:
    """Returns the information in the csv file, split into three parts:
    1) The extra information included in the csv file before the header row is encountered
    2) The headers themselves
    3) The information after the headers
    """
    extra_info = []
    headers = None
    header_info = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        non_header_reader = csv.reader(f)

        for non_header_line in non_header_reader:
            rows = ', '.join(non_header_line)
            if re.search(header_pattern, rows, re.VERBOSE):
                headers = non_header_line
                break
            extra_info.append(non_header_line)

        # switch to a dict reader to get the data under the header columns
        header_reader = csv.DictReader(f, fieldnames=headers)

        for header_line in header_reader:
            header_info.append(header_line)

    return CSVInfo(extra_info, headers, header_info)


def valid_csv_format_message() -> str:
    """Returns information about expected format for the movie list csv file."""
    message = dedent(
        f"""
    Could not find all the required column labels `Name`, `URL` and `Year`.
    
    Make sure those column labels occur within the first {MAX_CSV_ROWS_TO_FIND_HEADERS} lines of your
    csv file.
    
    The expected format looks similar to this 
    Note: The `Name`, `URL`, and `Year` columns can be in any order:

    │ ... │ ...    │ ...  │ ...                  │ ... │
    ├─────┼────────┼──────┼──────────────────────┼─────┤
    │ ... │ Name   │ Year │ URL                  │ ... │
    ├─────┼────────┼──────┼──────────────────────┼─────┤
    │ ... │ Amélie │ 2001 │ https://boxd.it/2aUc │ ... │
    ├─────┼────────┼──────┼──────────────────────┼─────┤
    │ ... │ RRR    │ 2022 │ https://boxd.it/ljDs │ ... │
    ├─────┼────────┼──────┼──────────────────────┼─────┤
    │ ... │ Oldboy │ 2003 │ https://boxd.it/29R2 │ ... │
    ├─────┼────────┼──────┼──────────────────────┼─────┤
    │ ... │ ...    │ ...  │ ...                  │ ... │
    
    Check your csv file columns and try again.
    """
    )

    return message
