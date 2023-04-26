from utils.csv_utils import *
import itertools


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


def test_required_columns_can_occur_in_any_order(tmp_path):
    arrangements = itertools.permutations(['Position', 'Name', 'Year', 'URL', 'Description'])
    for arrangement in arrangements:
        content = f"""
        Letterboxd list export v7,,,,
        Date,Name,Tags,URL,Description
        2023-04-17,A test lis,Sort by colour,The url,A test list.
        ,,,,
        {','.join(arrangement)}
        """
        csv_file = tmp_path / 'columns_in_some_order.csv'
        csv_file.write_text(content)
        assert is_valid_letterboxd_format(csv_file)
