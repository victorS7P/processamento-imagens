import numpy as np
from skimage import measure, feature
from scipy import ndimage as ndi

def PropertiesFn (image):
  bordas = feature.canny(image)
  preenchida = ndi.binary_fill_holes(bordas)
  return measure.regionprops_table(measure.label(preenchida), properties=('centroid', 'orientation', 'bbox', 'area', 'perimeter'))
Properties = {
  "name": "Detecção de Componentes",
  "function": PropertiesFn
}
