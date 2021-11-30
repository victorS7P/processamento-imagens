import cv2
import numpy as np
from utils import get_grayscale

def texture_segmentation(image):
    image_gray = get_grayscale(image)
    k = 45
    theta = np.pi/4
    theta2 = np.pi/2
    theta3 = 0
    theta4 = np.pi/-4
    kernel = cv2.getGaborKernel((k, k), 5.0, theta, 10.0, 0.9, 0, ktype= cv2.CV_32F)
    kernel2 = cv2.getGaborKernel((k, k), 5.0, theta2, 10.0, 0.9, 0, ktype= cv2.CV_32F)
    kernel3 = cv2.getGaborKernel((k, k), 5.0, theta3, 10.0, 0.9, 0, ktype= cv2.CV_32F)
    kernel4 = cv2.getGaborKernel((k, k), 5.0, theta4, 10.0, 0.9, 0, ktype= cv2.CV_32F)

    imagem = cv2.filter2D(image_gray, cv2.CV_8UC3, kernel+kernel2+kernel3+kernel4)
    return imagem   