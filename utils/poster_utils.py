"""Utility functions for handling the fetching and downloading of movie posters"""

import os
import re
import requests
from typing import Optional
from pathlib import Path, PurePath
from bs4 import BeautifulSoup

FILM_POSTER_URL_PATTERN = r'https:\/\/a\.ltrbxd\.com\/resized\/.*?\.jpg'


def create_posters_dir(parent_dir: str, dir_name: str) -> str:
    """Creates the directory in which the downloaded posters will be saved.

    Parameters
    ----------
    parent_dir : str
        The parent directory, inside which the poster directory will be created.
    dir_name : str
        The name of the poster directory that will be created.

    Returns
    -------
    str
        The full path of the poster directory.
    """
    folder_path = Path(PurePath(parent_dir) / Path(dir_name))

    if not Path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'{dir_name} folder created...')

    return str(folder_path)


def get_film_page_html(film_url: str) -> str:
    """Returns the contents (the html) of a film's letterboxd page.

    Parameters
    ----------
    film_url : str
        The Letterboxd url of this movie's page.

    Returns
    -------
    str
        The html contents of the movie's Letterboxd page.
    """
    film_page_html = requests.get(film_url).text
    return film_page_html


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


def get_poster_contents(film_poster_url: str) -> bytes:
    """Returns the raw content (bytes) of the film poster image that is located at the given url.

    Parameters
    ----------
    film_poster_url : str
        The url of the film poster image.

    Returns
    -------
    bytes
        The raw content (bytes) of the film poster image.
    """
    poster_contents = requests.get(film_poster_url).content
    return poster_contents


def download_poster(poster_contents: bytes, film_name: str, download_location: str, extension='.jpg') -> None:
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
    with open(picture_path, 'wb') as f:
        f.write(poster_contents)
