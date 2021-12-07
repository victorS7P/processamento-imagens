from utils import get_grayscale
import numpy as np 
from skimage.filters import threshold_local
from functions.aula02 import BlurFn

def binary_segmentation(image, threshold):
    image_gray = get_grayscale(image)
    classified = image_gray>threshold[0]/255
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

def convolucao(image, kernel):
  himagem = image.shape[0]
  wimagem = image.shape[1]

  hkernel = kernel.shape[0]
  wkernel = kernel.shape[1]

  h = hkernel//2
  w = wkernel//2
  
  imagemconv = np.zeros(image.shape)

  for linha in range(himagem):
    for coluna in range(wimagem):
      soma = 0
      for linhak in range(hkernel):
        for colunak in range(wkernel):
          if linha+linhak-h >= 0 and linha+linhak-h < himagem and coluna+colunak-w >= 0 and coluna+colunak-w < wimagem:
            soma += kernel[linhak][colunak] * image[linha+linhak-h][coluna+colunak-w]
      imagemconv[linha][coluna] = soma

  return imagemconv

def gx(image):
  image_gray = get_grayscale(image)
  image_blur = BlurFn(image_gray, [4])
  roberts_x = np.array([[1, 0], [0, -1]], dtype = np.float)
  return convolucao(image_blur,roberts_x)

def gy(image):
  image_gray = get_grayscale(image)
  image_blur = BlurFn(image_gray, [4])
  roberts_y = np.array([[0, 1], [-1, 0]], dtype = np.float)
  return convolucao(image_blur,roberts_y)

def roberts(image):
  image_x = gx(image)
  image_y = gy(image)
  
  gradient = np.sqrt(np.square(image_x) + np.square(image_y))
  gradient *= 255.0 / gradient.max()
  return gradient/255
  
  