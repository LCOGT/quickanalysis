import pytest
import requests
import numpy as np
from urllib.error import HTTPError

from quickanalysis.utils.load_data import check_if_s3_image_exists
from quickanalysis.utils.load_data import get_image_data

NONEXISTENT_FILE = "im a string not a filename"
VALID_FITS_FILENAME = "tst-test-20201112-00000058-EX10.fits.bz2"
VALID_TEXT_FILENAME = "tst-test-20201112-00000058-EX00.txt"


def test_check_if_s3_image_exists_good_filename():
    s3_directory = "data"
    assert check_if_s3_image_exists(VALID_FITS_FILENAME, s3_directory)


def test_check_if_s3_image_exists_bad_filename():
    s3_directory = "data"
    assert not check_if_s3_image_exists(NONEXISTENT_FILE, s3_directory)


def test_get_image_data():
    s3_directory = "data"
    data = get_image_data(VALID_FITS_FILENAME, s3_directory)
    assert isinstance(data, np.ndarray)


def test_get_image_data_invalid_filename():
    s3_directory = "data"
    with pytest.raises(Exception):
        data = get_image_data(NONEXISTENT_FILE, s3_directory)


def test_get_image_data_text_file():
    s3_directory = "data"
    with pytest.raises(Exception):
        data = get_image_data(VALID_TEXT_FILENAME, s3_directory)
