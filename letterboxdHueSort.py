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
)

parser = argparse.ArgumentParser()
parser.add_argument('film_list_csv', help='Absolute path of the csv file representing your letterboxd film list')
args = parser.parse_args()

film_csv_path: str = args.film_list_csv


def main():
    csv_path = get_csv_absolute_path(film_csv_path)

    if not is_valid_letterboxd_format(csv_path):
        sys.exit(valid_csv_format_message())

    csv_info = get_csv_sections(csv_path)
    
    # directory in which to save the posters
    posters_dir = create_posters_dir(parent_dir=str(PurePath(csv_path).parent), dir_name='posters')

    for film in csv_info.film_info:
        page = get_film_page_html(film['URL'])
        poster_url = get_poster_url(page)

        if poster_url:
            poster_content = get_poster_contents(poster_url)
            film_name = film['Name']
            download_poster(poster_contents=poster_content, download_location=posters_dir, film_name=film_name)
        else:
            print(f"Couldn't find poster for {film['Name']}")
            continue


if __name__ == '__main__':
    main()
