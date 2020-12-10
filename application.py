from flask import Flask
application = app = Flask(__name__)

from flask import Flask, request, jsonify
import json

from astropy.io import fits

from quickanalysis.utils import get_photonranch_image_url
from quickanalysis.utils import check_if_s3_image_exists
from quickanalysis.utils import data_array_from_url
from quickanalysis.analysis.profile_line import get_intensity_profile
from quickanalysis.analysis.profile_line import get_example_profile


@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"data":"welcome"})


@app.route('/lineprofile', methods=['POST'])
def lineprofile():
    """ Return a line profile.

    POST args:
        start (dict): 'x' and 'y' values for the line start point, in [0, 1]
        end (dict): same as start
        full_filename (str): photon ranch filename in s3, including the extension.

    Example post request:
    curl -X POST http://localhost:5000/lineprofile -F \
        'data={"start":{"x": 0, "y":0}, "end": {"x": 1, "y": 1}, 
        "full_filename": "tst-test-20201112-00000058-EX01.fits.bz2"}'

    """

    # parse args
    print(request.form['data'])
    form_data = json.loads(request.form['data'])
    start = (form_data['start']['x'], form_data['start']['y'])
    end = (form_data['end']['x'], form_data['end']['y'])
    full_filename = form_data['full_filename']

    if not check_if_s3_image_exists(full_filename):
        return jsonify({
            "success": False,
            "message": f"Image does not exist: {full_filename}."
        })

    image_url = get_photonranch_image_url(full_filename)
    data = data_array_from_url(image_url)
    profile = get_intensity_profile(data, start, end)
    return jsonify({
        "success": True,
        "start": start,
        "end": end,
        "data": profile,
    })

@app.route('/lineprofile/example', methods=['GET'])
def line_profile_example():

    profile = get_example_profile() 
    return jsonify({
        "data": profile
    })


if __name__ == "__main__":
    application.run()
