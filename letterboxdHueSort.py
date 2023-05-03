import argparse
import sys
from pathlib import Path, PurePath
from utils.csv_utils import (
    get_csv_absolute_path,
    is_valid_letterboxd_format,
    valid_csv_format_message,
    get_csv_sections,
)
from utils.poster_utils import (
    get_film_page_html,
    get_poster_url,
    get_poster_contents,
    download_poster,
    create_posters_dir,
    all_posters_downloaded,
    get_posters
)
import requests
from rich.console import Console
from utils.csv_utils import CSVInfo


parser = argparse.ArgumentParser()
parser.add_argument('film_list_csv', help='Absolute path of the csv file representing your letterboxd film list')
args = parser.parse_args()

film_csv_path: str = args.film_list_csv
console = Console(color_system='truecolor')


def main():
    csv_path = get_csv_absolute_path(film_csv_path)

    if not is_valid_letterboxd_format(csv_path):
        sys.exit(valid_csv_format_message())

    csv_sections = get_csv_sections(csv_path)

    posters_dir_name = 'posters'  # directory in which to save the posters
    csv_parent_dir = PurePath(csv_path).parent
    posters_dir_path = Path(csv_parent_dir) / Path(posters_dir_name)

    if not posters_dir_path.exists():
        msg = f'\n┣━ {posters_dir_name} folder created\n'
        posters_dir = create_posters_dir(str(PurePath(csv_path).parent), posters_dir_name, msg)
        get_posters(csv_sections, posters_dir_path, console)
    elif not all_posters_downloaded(csv_sections, Path(posters_dir_path)):
        get_posters(csv_sections, posters_dir_path, console)
    else:
        pass


if __name__ == '__main__':
    main()
