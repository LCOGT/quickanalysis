import numpy as np

def get_num_bins(bin_size, min_val, max_val):
  """Given the bin size, how many bins are necessary to cover the given range of values? 

  This is a helper method for computing image histograms. 

  Args:
    bin_size (int): how many values to count in each bin. Setting this to 1 provides maximum resolution. 
    min_val (int): set the lower bound for the histogram (ie. ignore values below this)
    max_val (int): set the upper bound for the histogram

  Returns:
    int: the number of bins to use in the histogram calculation.
  """

  # Range of values to cover
  val_range = max_val - min_val

  # How many times will our bin size fit in the given range (q), and what is the remainder (r)?
  q, r = divmod(val_range, bin_size)

  # Add one because we need num_bins * bin_size > range (not <= range). 
  return q + 1

def get_histogram(arr, bin_size=None, clip_percent=None, bitpix=16, exclude_zero=False):
  """Compute a histogram for the provided image data array.

  Args:
    arr (n-dimensional numpy array): the data to analyze
    bin_size (int): how many intensity values per bin (lower bin_size -> higher resolution data). 
                    if None: bin size will be automatically set so that the number of bins is < 5000.
    clip_percent (float): Compute the histogram without the <clip_percent> percentage of intensities (ie. skip the top
                          and bottom 5% by setting clip_percent=0.05)
                          If clip_percent==None, the histogram will use the full range of possible pixel intensities.
                          Note that if clip_percent==0, the histogram range will not exceed the min and max pixels. 
    bitpix (int): bits per pixel. Find total number of possible pixel values by computing 2**bitpix

  Returns:
    counts (numpy array of ints): number of counts in each bin
    edges (numpy array of floats): defines bins (i-th bin is anything between
                                   edges[i] and edges[i+1])
  """

  # Default range should include the whole image
  low_val = np.min(arr)
  high_val = np.max(arr)
  print(f"low val: {low_val}, high val: {high_val}")

  # Or use percentage clipping to determine the range (if clip_percent is specified)
  if clip_percent is not None:
    # Convert percentile from [0,1] to [0, 100]
    clip_percent *= 100

    # Compute clipping high/low values
    low_val = np.percentile(arr, clip_percent)
    high_val = np.percentile(arr, 100 - clip_percent)

  if exclude_zero and low_val == 0:
    low_val += 1

  ## Compute the bin edges

  # Automatically size the bins so that the number of bins is less than 5000.
  # This is to help rendering on the frontend. 
  # This code should be replaced when we implement 'levels of detail' functionality in the d3 graph. 
  if bin_size is None:
    for possible_bin_size in range (1,20):
      num_bins_candidate = get_num_bins(possible_bin_size, low_val, high_val)
      if num_bins_candidate < 5000:
        print('num_bins_candidate: ',num_bins_candidate)
        num_bins = num_bins_candidate
        bin_size = possible_bin_size
        print('bin_size: ', possible_bin_size)
        break

  # No auto bin sizes if a bin_size value is provided. 
  else:
    num_bins = get_num_bins(bin_size, low_val, high_val)

  #num_bins = get_num_bins(bin_size, low_val, high_val)
  num_bin_edges = num_bins + 1
  modified_low_val = low_val - 0.5  # center the bins around the interger counts we are measuring.
  # The last bin edge value should be low_val + (i * bin_size) + C = range, 
  # where i is an integer and 0 < C <= bin_size.
  modified_high_val = low_val + (num_bins * bin_size) + 1
  bin_edges = np.arange(low_val, modified_high_val, bin_size)


  counts, edges = np.histogram(arr, bins=bin_edges)
  print('number of counts: ', len(counts))
  return counts, edges
