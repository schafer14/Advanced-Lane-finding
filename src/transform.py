import cv2
import numpy as np
from numpy.linalg import inv


class Transform:
    # Create the perspective mapping at init time instead of run time.
    def __init__(self, src, from_size=(1280, 720), to_size=(800, 600)):
        self.src = src

        # Definable sizes for the new images
        self.from_size = from_size
        self.to_size = to_size

        dest = np.float32([[200, 0], [600, 0], [600, to_size[1]], [200, to_size[1]]])

        # Create and save the resulting warp matrix
        M = cv2.getPerspectiveTransform(self.src, dest)

        self.M = M
        self.invM = inv(M)

    def warp(self, img):
        return cv2.warpPerspective(img, self.M, self.to_size, flags=cv2.INTER_LINEAR)

    def unwarp(self, img):
        return cv2.warpPerspective(img, self.invM, self.from_size, flags=cv2.INTER_LINEAR)