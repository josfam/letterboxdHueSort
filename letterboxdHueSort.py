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
import requests
from rich.console import Console

HARD_ERROR_COLOR = 'deep_pink4'
IN_PROGRESS_COLOR = 'green'
SOFT_ERROR_COLOR = 'grey70'


parser = argparse.ArgumentParser()
parser.add_argument('film_list_csv', help='Absolute path of the csv file representing your letterboxd film list')
args = parser.parse_args()

film_csv_path: str = args.film_list_csv


def main():
    console = Console(color_system='truecolor')
    csv_path = get_csv_absolute_path(film_csv_path)

    if not is_valid_letterboxd_format(csv_path):
        sys.exit(valid_csv_format_message())



def all_posters_downloaded(csv_sections: CSVInfo, posters_dir_path: Path) -> bool:
    """Returns True if all the posters of the films in the csv file have been downloaded. Returns False otherwise.

    Parameters
    ----------
    csv_sections : CSVInfo
        The three sections of the csv, i.e.`extra_info`, `headers`, and `film_info`.
    posters_dir_path : Path
        The path representing the location of the posters directory, in which posters are downloaded.

    Returns
    -------
    bool
        True if all the posters of the films in the csv file have been downloaded, False otherwise.
    """
    poster_count = len(list(posters_dir_path.iterdir()))
    movie_count = len(csv_sections.film_info)
    return poster_count == movie_count


    img_extension = '.jpg'  # file extension with which posters will be saved

    for film in csv_info.film_info:
        film_url = film['URL']
        film_name = film['Name']
        print(f'\n ┃ {film_name.upper()}')

        # check if the poster already exists before trying to download it
        if Path.exists(Path(posters_dir) / Path( film_name + img_extension)):
            print(' ┗ Poster already exists. Skipping this film')
            continue

        try:
            msg = f' ┃ Searching film page'
            page_contents = get_film_page_html(film_url, msg)
        except requests.exceptions.ConnectionError:
            console.print(' ━┫ There seems to be a problem with your internet connection.\n', style=HARD_ERROR_COLOR)
            sys.exit()
        except KeyboardInterrupt:
            sys.exit('\n┗━ Goodbye for now ━━━\n')

        poster_url = get_poster_url(page_contents)

        if poster_url:
            console.print(' ┃ Found poster', style=IN_PROGRESS_COLOR)
            try:
                msg = ' ┃ Fetching poster'
                poster_content = get_poster_contents(poster_url, msg)
            except requests.exceptions.ConnectionError:
                console.print(' ━┫ There seems to be a problem with your internet connection.\n', style=HARD_ERROR_COLOR)
                sys.exit()
            except KeyboardInterrupt:
                sys.exit('\n┗━ Goodbye for now ━━━\n')

            msg = ' ┗ Saving poster'
            download_poster(poster_content, film_name, posters_dir, msg, img_extension)
        else:
            console.print(" ━┫ Couldn't find poster", style=SOFT_ERROR_COLOR)
            print()
            continue


if __name__ == '__main__':
    main()
