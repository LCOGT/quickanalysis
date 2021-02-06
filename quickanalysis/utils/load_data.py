import boto3
import numpy as np
from astropy.io import fits
from lru import lru_cache

from quickanalysis import settings
from quickanalysis.utils.useful import roundint

s3 = boto3.client('s3', settings.AWS_REGION)

URL_EXPIRATION = 3600

def check_if_s3_image_exists(full_filename):
    try:
        s3.head_object(
            Bucket=settings.S3_BUCKET,
            Key=f'data/{full_filename}'
        )
    except Exception as e:
        return False
    return True


@lru_cache(maxsize=20, expires=URL_EXPIRATION)
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


def get_image_subrect(image_array, x0, x1, y0, y1):
    ylen, xlen = np.shape(image_array)
    ystart = roundint(y0 * ylen)
    yend = roundint(y1 * ylen)
    xstart = roundint(x0 * xlen) 
    xend = roundint(x1 * xlen)
    return image_array[ystart:yend, xstart:xend]
