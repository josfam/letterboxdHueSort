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
    if not PurePath.is_absolute(PurePath(film_csv_path)):
        while True:
            message = dedent(
                """
            Please provide the full path of your films' csv file.
            (q to quit)
            full path > """
            )
            try:
                film_csv_path = input(message)
            except KeyboardInterrupt:
                sys.exit('\nGoodbye')

            if film_csv_path.lower() == 'q':
                sys.exit('Goodbye!')

            if not PurePath.is_absolute(PurePath(film_csv_path)):
                continue

            # the file must exist
            elif not Path.exists(Path(film_csv_path)):
                print('The file you provided does not exist. Try again.')
                continue

            # the existing file must be a .csv file
            elif '.csv' not in PurePath(film_csv_path).suffix:
                print('This file is not a .csv file. Try again.')
                continue
            else:
                break
    return film_csv_path


if __name__ == '__main__':
    main()
