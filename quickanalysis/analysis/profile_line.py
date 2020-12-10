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

    xlen, ylen = np.shape(image_data_array)
    xlen -= 1
    ylen -= 1

    startx, starty = start
    endx, endy = end

    p1 = [starty * ylen, startx * xlen]
    p2 = [endy * ylen, endx * xlen]

    # Extract intensity values along some profile line
    p = profile_line(image_data_array, p1, p2, mode="constant", cval=-1)

    return list(p)

def get_example_profile():
    
    example_file = 'tst-test-20201112-00000058-EX10.fits.bz2'
    file_url = get_photonranch_image_url(example_file)
    data = fits.getdata(file_url)
    start = (0, 0)
    end = (1, 1)
    profile = get_intensity_profile(data, start, end)
    return list(profile)

# Load some image
#I = fits.getdata('data/new1.fits')
#I = fits.getdata('data/saf-test.fits')

#print(type(I))
#print(np.shape(I))

#x0 = random.randint(0, np.shape(I)[0])
#x1 = random.randint(0, np.shape(I)[0])
#y0 = random.randint(0, np.shape(I)[1])
#y1 = random.randint(0, np.shape(I)[1])

#x0 = 0
#y0 = 0.3 * np.shape(I)[1]
#x1 = np.shape(I)[0] - 1
#y1 = 0.3 * np.shape(I)[1]

#start = [y0, min(x0, x1)]
#end = [y1, max(x0, x1)]
##x = [800, 2500]
##y = [1970, 2980]
#print(start, end)
#print(np.max(I))

## Extract intensity values along some profile line
#p = profile_line(I, start, end, mode="constant", cval=-1)

#fig, ax = plt.subplots(2,1,figsize=(15,20))
#ax[0].imshow(I,cmap="gist_gray")
#ax[0].plot([start[1], end[1]], [start[0], end[0]], color='#f33')
##ax[1].set_yscale('log')
#ax[1].plot(p)
#plt.show()