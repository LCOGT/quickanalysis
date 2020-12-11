import boto3
from astropy.io import fits
from quickanalysis import settings

s3 = boto3.client('s3', settings.AWS_REGION)


def get_photonranch_image_url(full_filename):
    params = {
        'Bucket': settings.S3_BUCKET,
        'Key': f'data/{full_filename}'
    }
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params=params,
        ExpiresIn=3600 # 1 hour
    )
    return url


def check_if_s3_image_exists(full_filename):
    try:
        s3.head_object(
            Bucket=settings.S3_BUCKET,
            Key=f'data/{full_filename}'
        )
    except Exception as e:
        return False
    return True


def data_array_from_url(url):
    return fits.getdata(url)

