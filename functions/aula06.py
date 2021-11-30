import numpy as np
from skimage import feature
from scipy import ndimage

from functions.aula02 import BlurFn
from utils import get_grayscale, get_height_width

def CannyFn (image, params):
  grayscale = get_grayscale(image)
  blur = BlurFn(grayscale, params)
  return feature.canny(blur, sigma=params[0]/100)
Canny = {
  "name": "Canny",
  "function": CannyFn
}

def FFTFn (image, params):
  grayscale = get_grayscale(image)

  dft = np.fft.fft2(grayscale)
  shift_dft = np.fft.fftshift(dft)

  rows, cols = get_height_width(grayscale)
  mask = np.ones((rows, cols), np.uint8)

  r = params[0]
  center = [rows//2, cols//2]

  x, y = np.ogrid[:rows, :cols]
  mask_area = ((x - center[0]) ** 2) + ((y - center[1]) ** 2) <= (r * r)

  mask[mask_area] = 0
  mask_shift = shift_dft * mask

  mag = np.log(1 + abs(mask_shift))
  inv_shift = np.fft.ifftshift(mask_shift)
  inv_dft = np.fft.ifft2(inv_shift)

  mag = np.log(1 + abs(inv_dft))

  return mag
FFT = {
  "name": "FFT",
  "function": FFTFn
}

def HighPassFn (image):
  kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
  ])

  return ndimage.convolve(image, kernel)
HighPass = {
  "name": "Passa Alta",
  "function": HighPassFn
}

def LowPassFn (image):
  kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
  ])

  return ndimage.convolve(image, kernel)
LowPass = {
  "name": "Passa Baixa",
  "function": LowPassFn
}
