import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from utils import select_image
from skimage import exposure

def histogram (image):
  hist  = np.zeros(256) 
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      hist[image[i][j]] += 1
  return hist
  
def exposure_function(image):
  img = select_image()
  match = exposure.match_histograms(image, img, multichannel=-1)
  return match
  

