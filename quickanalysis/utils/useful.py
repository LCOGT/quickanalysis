import numpy as np
from flask.json import JSONEncoder


def roundint(x):
  """ Round to the nearest integer in the traditional way (ie. <=.5 goes up, >.5 goes down). """
  return int(x + (0.5 if x > 0 else -0.5))

class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)