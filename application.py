from flask import Flask
from flask_cors import CORS, cross_origin
application = app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

from flask import Flask, request, jsonify, render_template, render_template_string
import json
from astropy.io import fits
from marshmallow import Schema, fields, ValidationError, validates_schema

from quickanalysis.utils.load_data import check_if_s3_image_exists
from quickanalysis.utils.load_data import get_image_data
from quickanalysis.analysis.profile_line import get_intensity_profile
from quickanalysis.analysis.profile_line import get_intensity_profile_input_plot


class LineProfileInput(Schema):
    """ Parse and validate input for the line profile endpoint """
    full_filename = fields.Str(required=True)
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
    x0 = float(request.args.get('x0'))
    x1 = float(request.args.get('x1'))
    y0 = float(request.args.get('y0'))
    y1 = float(request.args.get('y1'))

    data = get_image_data(filename)
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

    Example post request:
    curl -X POST http://localhost:5000/lineprofile -F \
        'data={"start":{"x": 0, "y":0}, "end": {"x": 1, "y": 1}, 
        "full_filename": "tst-test-20201112-00000058-EX01.fits.bz2"}'

    """

    try:
        # Validate and parse args
        args = LineProfileInput().load(json.loads(request.data))
        start = (args['start']['x'], args['start']['y'])
        end = (args['end']['x'], args['end']['y'])
        full_filename = args['full_filename']

        # Make sure the requested file exists
        if not check_if_s3_image_exists(full_filename):
            return jsonify({
                "success": False,
                "message": f"Image does not exist: {full_filename}."
            }), 400

        # Get the image data and compute a line profile
        data = get_image_data(full_filename)
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


if __name__ == "__main__":
    application.run()
