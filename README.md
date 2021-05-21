# QuickAnalysis

[![Build Status](https://travis-ci.com/LCOGT/quickanalysis.svg?branch=main)](https://travis-ci.com/LCOGT/quickanalysis)
[![Coverage Status](https://coveralls.io/repos/github/LCOGT/quickanalysis/badge.svg?branch=main)](https://coveralls.io/github/LCOGT/quickanalysis?branch=main)

## Server-side image analysis for Photon Ranch observing sessions

Users running a real-time observing session with the Photon Ranch web application need to verify the quality of their incoming images.
QuickAnalysis is a server for running image analysis tasks that will make this verification faster and easier than having users download images for local analysis.

## Analysis Tasks

This server is accessible at http://quickanalysis.photonranch.org/.
Available endpoints are described below:

### POST - /lineprofile

Given the filename of an image in photon ranch and a line (start and end point), return an array of intensities. The points defining the line are relative to the image dimensions. So (0.5, 0.5) would be a point in the middle of the image. See the following python example for usage details. 

```python
import requests, json
url = "http://quickanalysis.photonranch.org/lineprofile"
body = json.dumps({ 
    "full_filename": "tst-test-20201112-00000058-EX10.fits.bz2",             
    "s3_directory": "data",
    # return the intensity profile for the line spanning the top left to bottom right corners.
    "start": {
        "x": 0,
        "y": 0,
    },
    "end": {
        "x": 1,
        "y": 1,
    }
})
requests.post(url, body).json()
"""
{
    "success": true,
    "data": [ ... 260.0, 255.0, 237.0 ... ], 
    "start": [
        0, 
        0
    ], 
    "end": [
        1, 
        1
    ]
}
"""
```

## Local Development

### **Configure AWS Credentials**

This application is designed to work with the AWS configuration used by photon ranch. 
Ensure your system has the appropriate photon ranch [AWS credentials and config files](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) in order to run this application on your machine.

### **Set up a [virtual environment](https://docs.python.org/3/tutorial/venv.html)**

Using a virtual environment is highly recommended. Run the following commands from the base of this project. `(venv)`
is used to denote commands that should be run using your virtual environment.

    python3 -m venv venv
    source venv/bin/activate
    (venv) pip install -r requirements.txt

### **Run the tests**

    (venv) python -m pytest

### **Run the application**

    (venv) python application.py

The quickanalysis server should now be accessible from <http://127.0.0.1:5000>!
