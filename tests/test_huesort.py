from utils.csv_utils import *

def test_csv_cannot_be_empty(tmp_path):
    csv_file = tmp_path / 'empty.csv'
    csv_file.write_text('')
    assert not is_valid_letterboxd_format(csv_file)
