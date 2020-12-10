from flask import request
import json
import boto3
import numpy as np
from astropy.io import fits

s3 = boto3.client('s3', 'us-east-1')
bucket_name = 'photonranch-001'


def get_photonranch_image_url(full_filename):
    params = {
        'Bucket': bucket_name,
        'Key': f'data/{full_filename}'
    }
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params=params,
        ExpiresIn=3600 # 1 hour
    )
    print(url)

    return url


def check_if_s3_image_exists(full_filename):
    try:
        s3.head_object(
            Bucket=bucket_name,
            Key=f'data/{full_filename}'
        )
    except:
        return False
    return True



def data_array_from_url(url):
    #return fits.open(url)[0].data
    return fits.getdata(url)

