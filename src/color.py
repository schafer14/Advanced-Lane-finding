import cv2
import numpy as np


def color(img):
    LUV0 = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)[:, :, 0]

    LAB2 = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)[:, :, 2]

    combined_binary = np.zeros_like(LUV0)
    combined_binary[((LAB2 >= 155) & (LAB2 <= 200)) | (LUV0 > 225)] = 1

    return combined_binary