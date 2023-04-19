"""Utility functions for handling the fetching and downloading of movie posters"""

import os
import re
import requests
from typing import Optional
from pathlib import Path, PurePath

FILM_POSTER_URL_PATTERN = r'https:\/\/a\.ltrbxd\.com\/resized\/film-poster.*?\.jpg'


def create_posters_dir(parent_dir: str, dir_name: str) -> str:
    """Creates the directory in which the downloaded posters will be saved.

    The directory will be created inside the provided parent directory, and named with the provided
    directory name.

    Returns the location of the posters directory
    """
    folder_path = Path(PurePath(parent_dir) / Path(dir_name))

    if not Path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'{dir_name} folder created...')
    
    return str(folder_path)


def get_film_page_html(film_url: str) -> str:
    """Returns the contents (the html) of a film's letterboxd page, given the film's letterboxd url"""
    film_page_html = requests.get(film_url).text
    return film_page_html


def get_poster_url(film_page_contents: str, url_pattern=FILM_POSTER_URL_PATTERN) -> Optional[str]:
    """Returns the url of the film's poster, given the url of the film page itself.
    Returns None if there is no match (dictated by the url pattern) for a film poster.
    """
    if match := re.search(url_pattern, film_page_contents):
        poster_url = match.group(0)
        return poster_url
    return None


def get_poster_contents(film_poster_url: str) -> bytes:
    """Returns the raw content (bytes) of the film poster image that is located at the given url."""
    poster_contents = requests.get(film_poster_url).content
    return poster_contents


def download_poster(poster_contents: bytes, film_name: str, download_location: str) -> None:
    """Downloads the film poster's contents (bytes), and saves them in the provided download location.
    The image will be saved under a name that corresponds to the name of the film.
    """
    picture_path = str(Path(download_location) / Path(film_name))
    with open(picture_path, 'wb') as f:
        f.write(poster_contents)
