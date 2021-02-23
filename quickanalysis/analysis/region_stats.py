import numpy as np
from scipy import stats

def get_mode(arr):
  return stats.mode(arr.flatten())[0][0]

def get_median(arr):
    return np.median(arr)

def get_mean(arr):
    return np.mean(arr)

def get_min(arr):
    return np.min(arr)

def get_max(arr):
    return np.max(arr)

def get_std(arr):
    return np.std(arr)

def get_median_abs_deviation(arr):
    # NOTE: pixinsight's (v1.8.7) MAD calculation matches the output of scipy.stats.median_absolute_deviation, 
    # which is deprecated in favor of scipy.stats.median_abs_deviation. If matching pixinsight becomes a priority, 
    # we should swap algorithms.
    return stats.median_abs_deviation(arr.flatten())
