import numpy as np
import cv2 as cv

def RotateFn (image, params):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv.getRotationMatrix2D(image_center, params[0], 1.0)
  result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
  return result
Rotate = {
  "name": "Rotação",
  "function": RotateFn
}

def BlurFn (image, params):
  return cv.blur(image, (params[0], params[0])) if params[0] > 0 else image
Blur = {
    "name": "Desfoque",
    "function": BlurFn
}

def PixelateFn (image, params):
  pixels = (100 - params[0]) if params[0] != 100 else 1

  height, width, _ = image.shape
  temp = cv.resize(image, (pixels, pixels), interpolation=cv.INTER_LINEAR)
  return cv.resize(temp, (width, height), interpolation=cv.INTER_NEAREST)
Pixelate = {
    "name": "Pixelização",
    "function": PixelateFn
}