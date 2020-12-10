import pytest
import requests
import numpy as np
from urllib.error import HTTPError

from quickanalysis.utils import get_photonranch_image_url
from quickanalysis.utils import check_if_s3_image_exists
from quickanalysis.utils import data_array_from_url

NONEXISTANT_FILE = "im a string not a filename"
VALID_FITS_FILENAME = "tst-test-20201112-00000058-EX10.fits.bz2"
VALID_TEXT_FILENAME = "tst-test-20201112-00000058-EX00.txt"


def test_get_photonranch_image_url_good_filename():
    url = get_photonranch_image_url(VALID_FITS_FILENAME)
    status_code = requests.get(url).status_code
    assert status_code == 200


def test_get_photonranch_image_url_bad_filename():
    url = get_photonranch_image_url(NONEXISTANT_FILE)
    status_code = requests.get(url).status_code
    assert status_code == 404


def test_check_if_s3_image_exists_good_filename():
    assert check_if_s3_image_exists(VALID_FITS_FILENAME)


def test_check_if_s3_image_exists_bad_filename():
    assert not check_if_s3_image_exists(NONEXISTANT_FILE)


# The supplied download link points to a fits.bz2 file
def test_data_array_from_url():
    url = get_photonranch_image_url(VALID_FITS_FILENAME)
    data = data_array_from_url(url)
    assert isinstance(data, np.ndarray)


# The supplied download link does not point to a file
def test_data_array_from_bad_url():
    with pytest.raises(Exception):
        url = get_photonranch_image_url(NONEXISTANT_FILE)
        data = data_array_from_url(url)

# The supplied download link points to a text file. Should fail.
def test_data_array_from_text_url():
    with pytest.raises(Exception):
        url = get_photonranch_image_url(VALID_TEXT_FILENAME)
        data = data_array_from_url(url)
