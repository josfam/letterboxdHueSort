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
        message = dedent(
            """
            The path you provided is not a full path.
            Please provide the full path of your films' csv file.
            (q to quit)
            full path > """
        )
        try:
            film_csv_path = input(message)
        except KeyboardInterrupt:
            sys.exit('\nGoodbye')
        else:
            if film_csv_path.lower() == 'q':
                sys.exit('Goodbye!')

    # the file must exist
    while not Path.exists(Path(film_csv_path)):
        message = dedent(
            """
            The file you provided does not exist.
            Please re-enter the full path again.
            (q to quit)
            full path > """
        )
        try:
            film_csv_path = input(message)
        except KeyboardInterrupt:
            sys.exit('\nGoodbye')
        else:
            if film_csv_path.lower() == 'q':
                sys.exit('Goodbye!')

    # the existing file must be a .csv file
    while '.csv' not in PurePath(film_csv_path).suffix:
        message = dedent(
            """
            The file you provided is not a .csv file.
            Please re-enter the full path again.
            (q to quit)
            full path > """
        )
        try:
            film_csv_path = input(message)
        except KeyboardInterrupt:
            sys.exit('\nGoodbye')
        else:
            if film_csv_path.lower() == 'q':
                sys.exit('Goodbye!')

    return film_csv_path


if __name__ == '__main__':
    main()
