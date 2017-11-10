import numpy as np
import cv2
import glob
import os.path


nx = 9
ny = 6


class Calibrator:
    def __init__(self, image_path, nx=nx, ny=ny):
        """
        Calculates the camera matrix that can be used to distort and undistort images

        This is done on init time so runtime can be a little faster.
        """
        try:
            self.dist = np.load("../camera_cal/dist.npy")
            self.mtx = np.load("../camera_cal/mtx.npy")
        except:
            images = glob.glob(image_path)

            img_points = []
            obj_points = []

            objp = np.zeros((nx * ny, 3), np.float32)
            objp[:, : 2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

            for fname in images:
                img = cv2.imread(fname)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
                if ret:
                    img_points.append(corners)
                    obj_points.append(objp)

            img_size = (img.shape[1], img.shape[0])
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, img_size, None, None)
            self.dist = dist
            self.mtx = mtx
            np.save("../camera_cal/dist.npy", self.dist)
            np.save("../camera_cal/mtx.npy", self.mtx)

    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
