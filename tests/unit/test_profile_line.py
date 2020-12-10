import pytest
import numpy as np

from quickanalysis.analysis.profile_line import get_intensity_profile
from quickanalysis.analysis.profile_line import get_example_profile

@pytest.fixture
def x_gradient_image():
    # Build 9x9 grid with x gradient from 0 to 4 in 0.5 step increments
    lin = np.linspace(0,4, 9) 
    gradient_image_data,_ = np.meshgrid(lin, lin)
    return gradient_image_data


def test_profile_line_horizontal(x_gradient_image):

    dimx, dimy = np.shape(x_gradient_image)

    # Test a horizontal line across the middle
    start = (0, 0.5)
    end = (1, 0.5)
    profile = get_intensity_profile(x_gradient_image, start, end)

    # All values should be increasing (ie. different)
    assert len(set(profile)) == len(profile)


def test_profile_line_vertical(x_gradient_image):

    dimx, dimy = np.shape(x_gradient_image)

    # Test a verticle line across the middle
    start = (0.5, 0)
    end = (0.5, 1)
    profile = get_intensity_profile(x_gradient_image, start, end)

    # All values should be the same because the gradient is across x only.
    assert len(set(profile)) == 1


def test_get_example_profile():
    profile = get_example_profile()
    assert isinstance(profile, list)
