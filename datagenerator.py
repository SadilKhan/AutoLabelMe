import numpy as np
import os
import numpy as np
import pandas as pd
import numpy as np
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import PIL
from PIL import ImageOps,Image



class DataGenerator:
    def __init__(self):
        pass    

    # Image Transformation
    def rgb2gray(self,image):
        """ Transform to Grayscale """
        r, g, b = image[:,:,0], image[:,:,1], image[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray

    def plot_image(self,image):
        """Plotting Image. Return PIL image"""
        return Image.fromarray(np.uint8(image))

    def flaten_image(self,array):
        """ Flatten a numpy array """
        return array.flatten()

    def scale_image(self,array):
        """ Scale an array from 0-255 to 0-1 range"""
        return array/255

    def crop_image(self,image,x):
        """Cropping Image"""
        return image[x[0][1]:x[1][1],x[0][0]:x[1][0]]

    def rotate_image(self,image,angle,fill=True):
        """Rotation"""
        if type(image)==np.ndarray:
            first_value=image[0]
            image=self.plot_image(np.uint8(image))
        else:
            first_value=np.array(image)[0]
        image=np.array(image.rotate(angle))
        if fill:
            image=Image.fromarray(np.where(image==0,first_value,image))
        return image

    def resize_image(self,image,new_size):
        """Resize Image"""
        if type(image)==np.ndarray:
            image=self.plot_image(np.uint8(image))
        return image.resize(new_size)

    def flip_image(self,image):
        """Vertical Flip"""
        if type(image)==np.ndarray:
            image=self.plot_image(np.uint8(image))
        return ImageOps.flip(image)

    def mirror_image(self,image):
        """Horizontal Flip"""
        if type(image)==np.ndarray:
            image=self.plot_image(np.uint8(image))
        return ImageOps.mirror(image)

    def affine_transform(self,image,affine_matrix):
        """ Affine Transformation """
        if type(image)==np.ndarray:
            image=self.plot_image(np.uint8(image))
        shape=image.size
        return image.transform(shape,Image.AFFINE,affine_matrix,resample=Image.BILINEAR)








