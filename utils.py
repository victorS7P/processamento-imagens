import numpy as np

def keep_float_range (image):
  image = np.maximum(image, np.zeros(image.shape))
  image = np.minimum(image, 1 * np.ones(image.shape))
  return image