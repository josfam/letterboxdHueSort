from utils.csv_utils import *


def test_csv_cannot_be_empty(tmp_path):
    csv_file = tmp_path / 'empty.csv'
    csv_file.write_text('')
    assert not is_valid_letterboxd_format(csv_file)


def test_non_empty_csv_must_contain_required_columns(tmp_path):
    content = """
    Letterboxd list export v7,,,,
    Date,Name,Tags,URL,Description
    2023-04-17,A test lis,Sort by colour,The url,A test list.
    ,,,,
    """.strip()
    csv_file = tmp_path / 'no_columns.csv'
    csv_file.write_text(content)
    assert not is_valid_letterboxd_format(csv_file)
