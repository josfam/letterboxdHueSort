"""Utility functions for displaying progress bars"""

from typing import Optional
from rich.progress import Progress

PROGRESS_BAR_INCREASE = 0.05
BAR_COLOR = 'green'


def show_progress_bar(message: str, total: Optional[int] = None) -> None:
    """Shows a progress bar

    Parameters
    ----------
    message : str
        The message to be displayed, alongside the progress bar.
    total : int or None, Optional
        The total size of the information being downloaded.

        When total is provided, a "determinate" progress bar is displayed.
        An "indeterminate" progress bar is displayed if no total is given.
    """
    with Progress() as progress:
        if total:
            task = progress.add_task(f"[{BAR_COLOR}]{message}", total=total)
            while not progress.finished:
                progress.update(task, advance=PROGRESS_BAR_INCREASE)
        else:
            task = progress.add_task(f"[{BAR_COLOR}]{message}", total=None, start=False)
            progress.update(task)
