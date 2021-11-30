import numpy as np
from matplotlib import image
from tkinter import filedialog as fd

def keep_float_range (image):
  image = np.maximum(image, np.zeros(image.shape))
  image = np.minimum(image, 1 * np.ones(image.shape))
  return image

def get_height_width (image):
  return image.shape[0], image.shape[1]

def get_grayscale (image):
  return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140]) if len(image.shape) == 3 else image

def select_image():
  filetypes=[
    ('image files', ('.tiff', '.jpeg', '.png'))
  ]

  filename =  fd.askopenfile(
    title='Open a image',
    initialdir='~/Pictures',
    filetypes=filetypes
  )
  
  return image.imread(filename.name)
