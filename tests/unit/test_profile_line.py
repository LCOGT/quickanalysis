import pytest
import numpy as np

from quickanalysis.analysis.profile_line import get_intensity_profile

@pytest.fixture
def x_gradient_image():
    """
    Build a 2d numpy array to mimic the data from a fits file with a gradient
    in the x axis. 
    [[0.  0.5 1.  1.5 2.  2.5 3. ]
     [0.  0.5 1.  1.5 2.  2.5 3. ]
     [0.  0.5 1.  1.5 2.  2.5 3. ]
     [0.  0.5 1.  1.5 2.  2.5 3. ]
     [0.  0.5 1.  1.5 2.  2.5 3. ]
     [0.  0.5 1.  1.5 2.  2.5 3. ]
     [0.  0.5 1.  1.5 2.  2.5 3. ]]
    """
    lin = np.linspace(0,3, 7) 
    gradient_image_data, _ = np.meshgrid(lin, lin)
    return gradient_image_data

@pytest.fixture
def y_gradient_image():
    """
    Build a 2d numpy array to mimic the data from a fits file with a gradient
    in the y axis. 
    [[0.  0.  0.  0.  0.  0.  0. ]
     [0.5 0.5 0.5 0.5 0.5 0.5 0.5]
     [1.  1.  1.  1.  1.  1.  1. ]
     [1.5 1.5 1.5 1.5 1.5 1.5 1.5]
     [2.  2.  2.  2.  2.  2.  2. ]
     [2.5 2.5 2.5 2.5 2.5 2.5 2.5]
     [3.  3.  3.  3.  3.  3.  3. ]]
    """
    lin = np.linspace(0,3, 7) 
    _, gradient_image_data = np.meshgrid(lin, lin)
    return gradient_image_data

def test_profile_line_x0(x_gradient_image):
    """ Ensure that the x-axis has x=0 at the left, not right. """
    start = (0,0)
    end = (0, 1)
    # This should return an array of zeros (the left vertical line of the 
    # x gradient)
    profile = get_intensity_profile(x_gradient_image, start, end)
    assert sum(profile) == 0

def test_profile_line_y0(y_gradient_image):
    """ Ensure that the y-axis has y=0 at the bottom, not top. """
    start = (0,1)
    end = (1, 1)
    # This should return an array of zeros (the top horizontal line of the 
    # y gradient)
    profile = get_intensity_profile(y_gradient_image, start, end)
    assert sum(profile) == 0


def test_profile_line_horizontal_x_gradient(x_gradient_image):

    dimx, dimy = np.shape(x_gradient_image)

    # Test a horizontal line across the middle
    start = (0, 0.5)
    end = (1, 0.5)
    profile = get_intensity_profile(x_gradient_image, start, end)
    print(x_gradient_image)

    # All values should be increasing (ie. different)
    assert len(set(profile)) == len(profile)


def test_profile_line_vertical_x_gradient(x_gradient_image):

    dimx, dimy = np.shape(x_gradient_image)

    # Test a verticle line across the middle
    start = (0.5, 0)
    end = (0.5, 1)
    profile = get_intensity_profile(x_gradient_image, start, end)

    # All values should be the same because the gradient is across x only.
    assert len(set(profile)) == 1


def test_profile_line_horizontal_y_gradient(y_gradient_image):

    dimx, dimy = np.shape(y_gradient_image)

    # Test a horizontal line across the middle
    start = (0, 0.5)
    end = (1, 0.5)
    profile = get_intensity_profile(y_gradient_image, start, end)
    print(x_gradient_image)

    # All values should be the same because the gradient is across x only.
    assert len(set(profile)) == 1


def test_profile_line_vertical_y_gradient(y_gradient_image):

    dimx, dimy = np.shape(y_gradient_image)

    # Test a verticle line across the middle
    start = (0.5, 0)
    end = (0.5, 1)
    profile = get_intensity_profile(y_gradient_image, start, end)

    # All values should be increasing (ie. different)
    assert len(set(profile)) == len(profile)

