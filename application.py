from flask import Flask
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from flasgger.utils import swag_from
from quickanalysis.utils.useful import NumpyEncoder

application = app = Flask(__name__)
Swagger(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = NumpyEncoder

from flask import Flask, request, jsonify, render_template, render_template_string
import json
from astropy.io import fits
from marshmallow import Schema, fields, ValidationError, validates_schema

from quickanalysis.utils.load_data import check_if_s3_image_exists
from quickanalysis.utils.load_data import get_image_data
from quickanalysis.utils.load_data import get_subregion_rect
from quickanalysis.analysis.profile_line import get_intensity_profile
from quickanalysis.analysis.profile_line import get_intensity_profile_input_plot
from quickanalysis.analysis.histogram import get_histogram

from quickanalysis.analysis.region_stats import get_mode, get_median, get_mean, get_min, get_max, get_std, get_median_abs_deviation


class LineProfileInput(Schema):
    """ Parse and validate input for the line profile endpoint """
    full_filename = fields.Str(required=True)
    s3_directory = fields.Str(required=True)
    start = fields.Dict(keys=fields.Str(), values=fields.Float(), required=True)
    end = fields.Dict(keys=fields.Str(), values=fields.Float(), required=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_catalog(self, data, **kwargs):
        point_coords = [
            data['start']['x'], 
            data['start']['y'], 
            data['end']['x'], 
            data['end']['y']
        ]
        print(point_coords)
        for val in point_coords:
            if val < 0 or val > 1:
                raise ValidationError(
                    'Input coordinates must be between 0 and 1')


@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"data":"welcome"})


@app.route("/lineprofiledisplay", methods=["GET"])
def plotView():
    """ This is a route to visualize the line requested for the line profile."""
    filename = request.args.get('filename')
    s3_directory = request.args.get('s3_directory')
    x0 = float(request.args.get('x0'))
    x1 = float(request.args.get('x1'))
    y0 = float(request.args.get('y0'))
    y1 = float(request.args.get('y1'))

    data = get_image_data(filename, s3_directory)
    start = (x0, y0)
    end = (x1, y1)
    profile = get_intensity_profile(data, start, end)
    selection_plot = get_intensity_profile_input_plot(data, start, end)
    
    return render_template_string("<img src='{{ image }}'/><div>{{data}}</div>", image=selection_plot, data=profile)


@app.route('/lineprofile', methods=['POST'])
@cross_origin()
def lineprofile():
    """ Return a line profile.

    POST args:
        start (dict): 'x' and 'y' values for the line start point, in [0, 1]
        end (dict): same as start
        full_filename (str): photon ranch filename in s3, including the extension.
        s3_directory (str): the 'folder' that the image resides in s3. [ data | info-images | allsky ]

    Example post request:
    curl -X POST http://localhost:5000/lineprofile -F \
        'data={"start":{"x": 0, "y":0}, "end": {"x": 1, "y": 1}, 
        "full_filename": "tst-test-20201112-00000058-EX01.fits.bz2", "s3_directory": "data"}'

    """

    try:
        # Validate and parse args
        args = LineProfileInput().load(json.loads(request.data))
        start = (args['start']['x'], args['start']['y'])
        end = (args['end']['x'], args['end']['y'])
        full_filename = args['full_filename']
        s3_directory = args['s3_directory']

        # Make sure the requested file exists
        if not check_if_s3_image_exists(full_filename, s3_directory):
            return jsonify({
                "success": False,
                "message": f"Image does not exist: {s3_directory}/{full_filename}."
            }), 400

        # Get the image data and compute a line profile
        data = get_image_data(full_filename, s3_directory)
        profile = get_intensity_profile(data, start, end)

        response = jsonify({
            "success": True,
            "start": start,
            "end": end,
            "data": profile,
        })
        return response


    except ValidationError as e:
        return jsonify({
            "success": False,
            "message": f"Validation error: {str(e)}",
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
        }), 500


@app.route('/statistics', methods=['POST'])
@cross_origin()
@swag_from('endpoint_docs/image_statistics.yml')
def image_statistics(): 
    """ Return statistics for an image or subregion. """

    # TODO: input documentation and validation

    args = json.loads(request.data)
    full_filename = args['full_filename']
    s3_directory = args['s3_directory']

    # Make sure the requested file exists
    if not check_if_s3_image_exists(full_filename, s3_directory):
        return jsonify({
            "success": False,
            "message": f"Image does not exist: {s3_directory}/{full_filename}."
        }), 400

    image_data = get_image_data(full_filename, s3_directory)
    if 'subregion' in args.keys():
        coords = args['subregion']
        image_data = get_subregion_rect(image_data, coords['x0'], coords['x1'], coords['y0'], coords['y1'] )

    stats = {
        "median": get_median(image_data),
        "mean": get_mean(image_data),
        "mode": get_mode(image_data),
        "min": get_min(image_data),
        "max": get_max(image_data),
        "std": get_std(image_data),
        "median_abs_deviation": get_median_abs_deviation(image_data),
    }
    
    return jsonify({
        "success": True,
        "stats": stats,
        "params": json.loads(request.data)
    }), 200


@app.route('/histogram-clipped', methods=['POST'])
@cross_origin()
@swag_from('endpoint_docs/histogram.yml')
def histogram(): 
    """ Return statistics for an image or subregion. 
    
    POST Args:
        full_filename (str): full file name for analysis, including the file extensions. 
        s3_directory (str): the 'folder' that the image resides in s3. [ data | info-images | allsky ]
        clip_percent (float): percentile value of intensity to define min and max range of histogram
        subregion (dict): optional, analyze subregion of image
        subregion['shape'] (str): type of shape. Currently only supports 'rect'.
        subregion['x0'] (float): coordinate defining the rect subregion (in range [0,1])
        subregion['x1'] (float): 
        subregion['y0'] (float): 
        subregion['y1'] (float): 
    
    """

    # TODO: input documentation and validation

    args = json.loads(request.data)
    full_filename = args['full_filename']
    s3_directory = args['s3_directory']
    clip_percent = args['clip_percent']
    print(full_filename, clip_percent)

    # Make sure the requested file exists
    if not check_if_s3_image_exists(full_filename, s3_directory):
        return jsonify({
            "success": False,
            "message": f"Image does not exist: {s3_directory}/{full_filename}."
        }), 400

    image_data = get_image_data(full_filename, s3_directory)
    if 'subregion' in args.keys():
        coords = args['subregion']
        image_data = get_subregion_rect(image_data, coords['x0'], coords['x1'], coords['y0'], coords['y1'] )

    counts, edges = get_histogram(image_data, clip_percent=clip_percent)
    
    return jsonify({
        "success": True,
        "histogram": {
            "counts": counts,
            "edges": edges,
            "stats": {
                "median": get_median(image_data),
                "mean": get_mean(image_data),
                "mode": get_mode(image_data),
                "min": get_min(image_data),
                "max": get_max(image_data),
            }
        },
        "params": json.loads(request.data)
    }), 200


if __name__ == "__main__":
    application.run()
