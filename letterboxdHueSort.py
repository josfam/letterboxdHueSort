from pathlib import Path, PurePath
import argparse
from textwrap import dedent
import sys

parser = argparse.ArgumentParser()
parser.add_argument('film_list_csv', help='Absolute path of the csv file representing your letterboxd film list')
args = parser.parse_args()

film_csv_path: str = args.film_list_csv


def main():
    csv_path = get_csv_absolute_path(film_csv_path)



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


if __name__ == '__main__':
    main()
