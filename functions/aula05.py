from utils import get_grayscale
import numpy as np 
from skimage.filters import threshold_local

def binary_segmentation(image, threshold):
    image_gray = get_grayscale(image)
    classified = image_gray>threshold[0]/100
    return classified 

Segmentation = {
  "name": "Segmentation",
  "function": binary_segmentation
}

def automatic_segmentation(image, limiar):
  image_gray = get_grayscale(image)
  if(limiar == 0):
    threshold = otsu(image_gray)
  else:
    threshold = threshold_local(image_gray, 15, offset = 10)
  classified = image_gray>threshold
  return classified

def otsu(imagem):
  qntPixels = imagem.size
  peso_media = 1.0/qntPixels
  histograma, bins = np.histogram(imagem, np.arange(0, 257))
  limiar = -1
  valor = -1
  intensidades = np.arange(256)

  for t in bins[1:-1]:
    pc1 = np.sum(histograma[:t])
    pc2 = np.sum(histograma[t:])
    peso1 = pc1 * peso_media
    peso2 = pc2 * peso_media

    mc1 = np.sum(intensidades[:t]*histograma[:t])/pc1
    mc2 = np.sum(intensidades[t:]*histograma[t:])/pc2

    temp = peso1 * peso2 * (mc1 - mc2) ** 2 

    if temp > valor:
      limiar = t
      valor = temp
  return limiar 
  
    
    