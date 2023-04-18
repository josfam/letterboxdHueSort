from pathlib import Path, PurePath
import argparse
from textwrap import dedent
import sys

parser = argparse.ArgumentParser()
parser.add_argument('film_list_csv', help='Absolute path of the csv file representing your letterboxd film list')
args = parser.parse_args()

film_csv_path: str = args.film_list_csv


def main():
    csv_path = get_proper_csv_path(film_csv_path)


def get_proper_csv_path(film_csv_path: str) -> str:
    """Returns the absolute path of an existing csv file"""
    # only absolute paths are accepted
    while not PurePath.is_absolute(PurePath(film_csv_path)):
        short_message = 'The path you provided is not a full path.'
        film_csv_path = ask_for_csv_path(short_message)

    # the file must exist
    while not Path.exists(Path(film_csv_path)):
        short_message = 'The file you provided does not exist.'
        film_csv_path = ask_for_csv_path(short_message)

    # the existing file must be a .csv file
    while '.csv' not in PurePath(film_csv_path).suffix:
        short_message = 'The file you provided is not a .csv file.'
        film_csv_path = ask_for_csv_path(short_message)

    return film_csv_path


def ask_for_csv_path(short_message: str) -> str:
    """Asks the user for the path of the film csv file.
    The message displayed is a combination of a short message, and a message that asks
    for the absolute path.
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


if __name__ == '__main__':
    main()
