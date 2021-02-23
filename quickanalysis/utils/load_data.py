import boto3
import numpy as np
from astropy.io import fits
from cachetools import cached, TTLCache

from quickanalysis import settings
from quickanalysis.utils.useful import roundint

s3 = boto3.client('s3', settings.AWS_REGION)

URL_EXPIRATION = 3600
MAX_CACHE_SIZE = 1e8  # the max `sys.getsizeof(x)` size for the cache

def check_if_s3_image_exists(full_filename):
    try:
        s3.head_object(
            Bucket=settings.S3_BUCKET,
            Key=f'data/{full_filename}'
        )
    except Exception as e:
        return False
    return True


@cached(cache=TTLCache(maxsize=1024, ttl=URL_EXPIRATION))
def get_image_data(full_filename):
    params = {
        'Bucket': settings.S3_BUCKET,
        'Key': f'data/{full_filename}'
    }
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params=params,
        ExpiresIn=URL_EXPIRATION
    )
    return fits.getdata(url)


def get_subregion_rect(image_array, x0, x1, y0, y1):
    """ Return the rectangular selection from an image array.

    Note: x=0,y=0 is the top left corner of the image.

    Args:
        x0 (float in [0,1]): x coordinate for one corner of the region.
        y0 (float in [0,1]): y coordinate for one corner of the region.
        x1 (float in [0,1]): x coordinate for the other corner of the region.
        y1 (float in [0,1]): y coordinate for the other corner of the region.
    
    Returns:
        2-d numpy array of pixel values.
    """

    # Compute the full pixel dimensions
    ylen, xlen = np.shape(image_array)

    ystart = np.rint(min(y0, y1) * ylen).astype(int)
    # Scale the subregion coordinates by the image dimensions
    yend =   np.rint(max(y1, y1) * ylen).astype(int)
    xstart = np.rint(min(x0, x1) * xlen).astype(int) 
    xend =   np.rint(max(x0, x1) * xlen).astype(int)
    return image_array[ystart:yend, xstart:xend]
