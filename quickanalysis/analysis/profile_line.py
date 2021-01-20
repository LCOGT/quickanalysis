import io
import base64
import numpy as np
from skimage.measure import profile_line
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from auto_stretch.stretch import Stretch

def get_pixel_dimensions(image_data_array, start, end):
    ''' Compute pixel coordinate values based on image dimensions and relative
    coordinats.

    Args: 
        image_data_array (2d numpy array)
        start (tuple[float]): x, y point for the start of the line, denoted by 
            fraction of size (value will be between 0 and 1)
        end (tuple[float]): same as start
    
    Return: 
        dict: float values for x0, y0, x1, y1 describing the line coordinates
                in pixels.
    '''
    # Get the x,y dimensions so that we can calculate the line coordinates.
    ylen, xlen = np.shape(image_data_array)
    xlen -= 1
    ylen -= 1

    # Convert the units from relative dimensions to pixels
    x0 = start[0] * xlen
    x1 = end[0] * xlen
    y0 = start[1] * ylen
    y1 = end[1] * ylen
    
    return (x0, y0, x1, y1)
        

def get_intensity_profile(image_data_array, start, end):
    ''' Compute an intensity profile between a start and end point.

    Args: 
        image_data_array (2d numpy array)
        start (tuple[float]): x, y point for the start of the line, denoted by 
            fraction of size (value will be between 0 and 1)
        end (tuple[float]): same as start
    
    Return: 
        List: intensity values between start and end point.
    '''

    x0, y0, x1, y1 = get_pixel_dimensions(image_data_array, start, end)

    # Extract intensity values along some profile line
    # This method expects y=0 to be the top of the image. 
    p = profile_line(image_data_array, [y0, x0], [y1, x1], mode="constant", cval=-1)

    return list(p)


def get_intensity_profile_input_plot(image_data_array, start, end):
    ''' Create a png plot of the image overlayed with the input line.

    This is useful for visualizing the analysis that is requested.

    Args: 
        image_data_array (2d numpy array)
        start (tuple[float]): x, y point for the start of the line, denoted by 
            fraction of size (value will be between 0 and 1)
        end (tuple[float]): same as start
    
    Return: 
        Str: png represented by a base 64 string
    '''

    x0, y0, x1, y1 = get_pixel_dimensions(image_data_array, start, end)

    # Generate plot of image and line selection overlayed.
    # This is useful for visualizing what is happening. 
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("line used for plot")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    axis.imshow(Stretch().stretch(image_data_array), cmap='Greys')
    axis.plot( [x0, x1], [y0, y1], color="#f33")

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return pngImageB64String