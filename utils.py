import numpy as np

def keep_float_range (image):
  image = np.maximum(image, np.zeros(image.shape))
  image = np.minimum(image, 1 * np.ones(image.shape))
  return image

def get_height_width (image):
  return image.shape[0], image.shape[1]

def get_grayscale (image):
  return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140]) if len(image.shape) == 3 else image