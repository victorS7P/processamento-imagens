import numpy as np
import cv2 as cv

from skimage import feature, measure
from scipy import ndimage as ndi

from functions.aula06 import CannyFn
from utils import get_grayscale

def HoughLinesFn (image, params):
  bordas = CannyFn(image, params)
  linhas = cv.HoughLines(bordas, 1, np.pi/180, 150)

  saida = np.copy(bordas)
  for linha in linhas:
    rho, tetha = linha[0]

    a = np.cos(tetha)
    b = np.sin(tetha)

    x0 = int(a * rho)
    y0 = int(b * rho)

    x1 = int(x0 + (1000 * -b))
    y1 = int(y0 + (1000 *  a))

    x2 = int(x0 - (1000 * -b))
    y2 = int(y0 - (1000 *  a))

    pt1 = (x1, y1)
    pt2 = (x2, y2)

    cv.line(saida, pt1, pt2, (255, 0, 0), 3, cv.LINE_AA)

  return saida
HoughLines = {
  "name": "Hough Linhas",
  "function": HoughLinesFn
}

def HoughCirclesFn (image, params):
  gray = get_grayscale(image)
  gray = (gray*255).astype(np.uint8)
  blur = cv.medianBlur(gray, params[0])

  circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 3, 2, None, param1=100, param2=100, minRadius=10, maxRadius=int(image.shape[0]/4))
  saida = np.copy(gray)

  for circle in circles[0]:
    x, y, r = circle
    x = int(x)
    y = int(y)
    r = int(r)

    cv.circle(saida, (x, y), r, (255, 0, 0), 2)
    cv.circle(saida, (x, y), 1, (255, 0, 0), 2)

  return (saida/255).astype(np.float32)
HoughCircles = {
  "name": "Hough Linhas",
  "function": HoughCirclesFn
}

def ComponentsFn (image):
  bordas = feature.canny(image)
  preenchida = ndi.binary_fill_holes(bordas)
  return (measure.label(preenchida)/64.0)
Components = {
  "name": "Detecção de Componentes",
  "function": ComponentsFn
}
