import numpy as np
from skimage import restoration, util

from functions.aula02 import BlurFn

def SharpnessFn (image, params):
  sigma = params[0]
  blurred = BlurFn(image, [sigma])
  return float(sigma + 1) * image - float(sigma) * blurred
Sharpness = {
  "name": "Nitidez",
  "function": SharpnessFn
}

#TODO: Criar seletor para escolher tipo do ruído
def NoiseFn (image, params):
  return util.random_noise(image, mode='speckle', var=params[0]/100, seed=1)
Noise = {
  "name": "Ruído",
  "function": NoiseFn
}

def NoiseCleanFn (image, params):
  sigma = np.mean(restoration.estimate_sigma(image, multichannel=True))
  return restoration.denoise_nl_means(image, h=(params[0]/100)*sigma, sigma=sigma, patch_size=3, patch_distance=4, multichannel=True)
NoiseClean = {
  "name": "Ruído",
  "function": NoiseCleanFn
}