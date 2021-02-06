import numpy as np


def roundint(x):
  """ Round to the nearest integer in the traditional way (ie. <=.5 goes up, >.5 goes down). """
  return int(x + (0.5 if x > 0 else -0.5))
