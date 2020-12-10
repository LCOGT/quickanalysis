import random
import numpy as np

# https://scikit-image.org/docs/dev/api/skimage.measure.html#profile-line
from skimage.measure import profile_line
from skimage import io
from astropy.io import fits
from auto_stretch.stretch import Stretch

from quickanalysis.utils import get_photonranch_image_url


def get_intensity_profile(image_data_array, start, end):
    ''' Compute an intensity profile between a start and end point.

    Args: 
        image_data_array (2d numpy array)
        start (tuple[float]): x, y point for the start of the line, denoted by 
            fraction of size (value will be between 0 and 1)
        end (tuple[float]): same as start
    
    Return: 
        List: intensity values between start and end point.
    '''

    # Get the x,y dimensions so that we can calculate the line coordinates.
    xlen, ylen = np.shape(image_data_array)
    xlen -= 1
    ylen -= 1

    # expand the start/end tuples containing (x,y) values.
    startx, starty = start
    endx, endy = end

    # The skimage profile_line method takes points with the order [y, x].
    p1 = [starty * ylen, startx * xlen]
    p2 = [endy * ylen, endx * xlen]

    # the skimage profile_line method also starts with y=0 at the top of the
    # image. We want y=0 to be the bottom to match "familiar" xy coordinates.
    p1[0] = ylen - p1[0]
    p2[0] = ylen - p2[0]

    # Extract intensity values along some profile line
    p = profile_line(image_data_array, p1, p2, mode="constant", cval=-1)

    return list(p)
