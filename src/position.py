import cv2


def position(right_fit, left_fit, img):
    width = 800
    height = 600

    # Find the position of the left lane and right lane at the bottom of the image
    right_0 = right_fit[0] * height ** 2 + right_fit[1] * height + right_fit[2]
    left_0 = left_fit[0] * height ** 2 + left_fit[1] * height + left_fit[2]

    xm_per_pix = 3.7 / 700  # meters per pixel in x dimension

    # The mid point of the lane in pixel coordinates
    mid = ((left_0 - right_0) / 2) + right_0

    # The number of pixels the mid point of the lane is off the image midpoint
    pixels = width / 2 - mid

    # Draw for demonstration
    cv2.circle(img, (int(right_0), 585), 3, (255, 255, 0), 4)
    cv2.circle(img, (int(left_0), 585), 3, (0, 255, 0), 4)
    cv2.circle(img, (int(mid), 585), 3, (0, 255, 255), 4)

    # I have to scale this further because I used weird dimensions for my warping
    return pixels * xm_per_pix * 1280 / width, img
