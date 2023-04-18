import argparse
import sys
from utils.csv_utils import get_csv_absolute_path, is_valid_letterboxd_format, valid_csv_format_message

parser = argparse.ArgumentParser()
parser.add_argument('film_list_csv', help='Absolute path of the csv file representing your letterboxd film list')
args = parser.parse_args()

film_csv_path: str = args.film_list_csv


def main():
    csv_path = get_csv_absolute_path(film_csv_path)
    if not is_valid_letterboxd_format(csv_path):
        sys.exit(valid_csv_format_message())


if __name__ == '__main__':
    main()
