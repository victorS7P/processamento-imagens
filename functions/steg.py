from copy import deepcopy
import numpy as np

from utils import get_height_width 

class Steg():
  string_delimiter  = "(>'')>"

  @staticmethod
  def data_to_binary (data):
    if type(data) == str:
      return ''.join([
        format(ord(i), '08b') for i in data
      ])
    
    if type(data) == bytes or type(data) == np.ndarray:
      return [
        format(i, '08b') for i in data
      ]

    if type(data) == int or type(data) == np.uint8:
      return format(data, '08b')

  @staticmethod
  def encode_string (image, data):
    image = image.astype(np.float64)
    image = 255 * image
    image = image.astype(np.uint8)

    is_rgb = len(image.shape) == 3
    
    binary_data = Steg.data_to_binary(data) + Steg.data_to_binary(Steg.string_delimiter)
    data_len = len(binary_data)

    x, y = get_height_width(image)
    z = 3 if is_rgb else 1

    max_bytes = (x * y * z) // 8

    if (data_len > max_bytes):
      raise ValueError('Insufficient bytes, need a bigger image!')

    data_index = 0
    new_image = deepcopy(image)
    
    for i in range(x): 
      for j in range(y):
        if is_rgb:
          r, g, b, *_ = Steg.data_to_binary(image[i][j])

          if (data_index < data_len):
            new_image[i][j][0] = int(r[:-1] + binary_data[data_index], 2)
            data_index += 1

          if (data_index < data_len):
            new_image[i][j][1] = int(g[:-1] + binary_data[data_index], 2)
            data_index += 1

          if (data_index < data_len):
            new_image[i][j][2] = int(b[:-1] + binary_data[data_index], 2)
            data_index += 1

          if (data_index >= data_len):
            break
        else:
          bit = Steg.data_to_binary(image[i][j])

          if (data_index < data_len):
            new_image[i][j] = int(bit[:-1] + binary_data[data_index], 2)
            data_index += 1

          if (data_index >= data_len):
            break

    new_image = new_image.astype(np.float64)
    return new_image / 255
    
  @staticmethod
  def pick_string (image):
    image = image.astype(np.float64)
    image = 255 * image
    image = image.astype(np.uint8)

    is_rgb = len(image.shape) == 3

    binary_data = ""
    decoded_data = ""

    x, y = get_height_width(image)

    for i in range(x): 
      for j in range(y): 
        if is_rgb:
          r, g, b, *_ = Steg.data_to_binary(image[i][j])

          binary_data += r[-1]
          binary_data += g[-1]
          binary_data += b[-1]
        else:
          bit = Steg.data_to_binary(image[i][j])
          binary_data += bit[-1]
          

    all_bytes = [
      binary_data[i: i+8] for i in range(0, len(binary_data), 8)
    ]

    for byte in all_bytes:
      decoded_data += chr(int(byte, 2))

      if (decoded_data[-len(Steg.string_delimiter):] == Steg.string_delimiter):
        return decoded_data[:-len(Steg.string_delimiter)]

    return None

def StegEncodeFn (image, params):
  return Steg.encode_string(image, params[0])
StegEncode = {
    "name": "Codificar Mensagem",
    "function": StegEncodeFn
}

def StegDecodeFn (image):
  return Steg.pick_string(image)
StegDecode = {
    "name": "Mensagem Codificada",
    "function": StegDecodeFn
}
