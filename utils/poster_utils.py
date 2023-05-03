"""Utility functions for handling the fetching and downloading of movie posters"""

import os
import re
import requests
from typing import Optional
from pathlib import Path, PurePath
from bs4 import BeautifulSoup
from utils.progress_utils import show_progress_bar
from typing import Callable, Optional
from PIL import Image
from utils.csv_utils import CSVInfo
from rich.console import Console
import io
import sys


FILM_POSTER_URL_PATTERN = r'https:\/\/a\.ltrbxd\.com\/resized\/.*?\.jpg'
SHRINK_FACTOR = 2
HARD_ERROR_COLOR = 'deep_pink4'
IN_PROGRESS_COLOR = 'green'
SOFT_ERROR_COLOR = 'grey70'

def create_posters_dir(parent_dir: str, dir_name: str, msg: str) -> str:
    """Creates the directory in which the downloaded posters will be saved.

    Parameters
    ----------
    parent_dir : str
        The parent directory, inside which the poster directory will be created.
    dir_name : str
        The name of the poster directory that will be created.
    msg : str
        The message to show when after creating the folder.
    
    Returns
    -------
    str
        The full path of the poster directory.
    """
    folder_path = Path(PurePath(parent_dir) / Path(dir_name))

    if not Path.exists(folder_path):
        os.makedirs(folder_path)
        print(msg)

    return str(folder_path)


def get_film_page_html(
    film_url: str, msg: str, progress_indicator: Callable[[str, Optional[int]], None] = show_progress_bar
) -> str:
    """Returns the contents (the html) of a film's letterboxd page.

    Parameters
    ----------
    film_url : str
        The Letterboxd url of this movie's page.
    msg : str
        The message to show when showing the progress indicator.
    progress_indicator : callable[[str, Optional[int]], None]
        A callable function that shows a progress bar.

        The function takes a string that will be the message displayed alongside the progress bar.
        Optionally, an integer representing the total size of data being processed can be provided.

    Returns
    -------
    str
        The html contents of the movie's Letterboxd page.
    """
    try:
        film_page_html = requests.get(film_url, stream=True)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError

    total = film_page_html.headers.get('content-length')

    if not total:
        progress_indicator(msg, None)
    else:
        progress_indicator(msg, int(total))
    return film_page_html.text


def get_poster_url(film_page_contents: str, url_pattern: str = FILM_POSTER_URL_PATTERN) -> Optional[str]:
    """Returns the url of the film's poster, given the url of the film page itself.
    Returns None if there is no match (dictated by the url pattern) for a film poster.

    Parameters
    ----------
    film_page_contents : str
        The content (html) of the film's page on Letterboxd.
    url_pattern : str, optional
        The pattern with which to match a film poster's url, which is located in the `film_page_contents`.

    Returns
    -------
    str or None
        The film poster's url, or None if no url that matched the `url_pattern` was found.
    """
    soup = BeautifulSoup(film_page_contents, 'html.parser')

    # find the poster links in the script tags of the page
    script_tags = str(soup.find_all('script'))

    if match := re.search(url_pattern, script_tags):
        poster_url = match.group(0)
        return poster_url
    return None


def get_poster_contents(
    film_poster_url: str, msg: str, progress_indicator: Callable[[str, Optional[int]], None] = show_progress_bar
) -> bytes:
    """Returns the raw content (bytes) of the film poster image that is located at the given url.

    Parameters
    ----------
    film_poster_url : str
        The url of the film poster image.
    msg : str
        The message to show when showing the progress indicator.
    progress_indicator : callable[[str, Optional[int]], None]
        A callable function that shows a progress bar.

        The function takes a string that will be the message displayed alongside the progress bar.
        Optionally, an integer representing the total size of data being processed can be provided.
    Returns
    -------
    bytes
        The raw content (bytes) of the film poster image.
    """
    try:
        poster_contents = requests.get(film_poster_url)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError

    total = poster_contents.headers.get('content-length')

    if not total:
        progress_indicator(msg, None)
    else:
        progress_indicator(msg, int(total))
    return poster_contents.content


def download_poster(
    poster_contents: bytes,
    film_name: str,
    download_location: str,
    msg: str,
    extension='.jpg',
    progress_indicator: Callable[[str, Optional[int]], None] = show_progress_bar,
) -> None:
    """Downloads the film poster's contents (bytes), and saves them in the provided download location.
    The image will be saved under a name that corresponds to the name of the film, and under the provided
    file extension.

    Parameters
    ----------
    poster_contents : bytes
        The raw byes that represent the contents of the film poster.
    film_name : str
        The name with which the poster will be saved after being downloaded.
    download_location : str
        The full path (absolute path) representing the location in which the film poster will be downloaded.
    extension : str, optional
        The file extension that the film poster will be saved with.

    Returns
    -------
    None
    """
    picture_path = str(Path(download_location) / Path(film_name + extension))

    with Image.open(io.BytesIO(poster_contents)) as im:
        smaller_dims = (im.width // SHRINK_FACTOR, im.height // SHRINK_FACTOR)
        resized = im.resize(smaller_dims) # save memory by saving a smaller version of the poster
        resized.save(picture_path)
        progress_indicator(msg, None)


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


def get_posters(csv_sections: CSVInfo, posters_dir: Path, console: Console) -> None:
    """Finds and downloads the posters for the films listed in the csv file.

    Parameters
    ----------
    csv_sections : CSVInfo
        The three sections of the csv, i.e.`extra_info`, `headers`, and `film_info`.
    posters_dir : Path
        The path representing the location of the posters directory, in which posters are downloaded.
    console : Console
        A Console object from the `rich` library, that is used to display colors and other styles.

    Returns
    -------
    None
    """
    img_extension = '.jpg'  # file extension with which posters will be saved
    for film in csv_sections.film_info:
        film_url = film['URL']
        film_name = film['Name']
        print(f'\n ┃ {film_name.upper()}')

        # check if the poster already exists before trying to download it
        if Path.exists(Path(posters_dir) / Path(film_name + img_extension)):
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
                console.print(
                    ' ━┫ There seems to be a problem with your internet connection.\n', style=HARD_ERROR_COLOR
                )
                sys.exit()
            except KeyboardInterrupt:
                sys.exit('\n┗━ Goodbye for now ━━━\n')

            msg = ' ┗ Saving poster'
            download_poster(poster_content, film_name, str(posters_dir), msg, img_extension)
        else:
            console.print(" ━┫ Couldn't find poster", style=SOFT_ERROR_COLOR)
            print()
            continue
