import numpy as np
import cv2
import matplotlib.pyplot as plt

plt.interactive(False)


def lines(image, n_windows=10):
    # Create a histogram of the bottom of the image
    histogram = np.sum(image[image.shape[0] // 2:, :], axis=0)

    # Create a color image to return
    out_image = np.dstack((image, image, image)) * 255

    # Find the start of maximum points
    midpoint = np.int(histogram.shape[0] / 2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    window_height = np.int(image.shape[0] / n_windows)

    # Set the first left position and right position and this will be updated for each iteration of the sliding window
    leftx_curr = leftx_base
    rightx_curr = rightx_base

    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = image.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Create the length of the rectangle to draw on the image
    win_len = 100 # this is actually half the window size

    # Define the minimum number of pixels needed to update teh current positions
    minpix = 50

    left_lane_inds = []
    right_lane_inds = []

    for i, window in enumerate(range(n_windows)):
        # LEFT WINDOW
        # Get window bounderies
        y_low = image.shape[0] - (window + 1) * window_height
        y_high = image.shape[0] - window * window_height

        # Find the left and right x coordinate of the rect
        rect_x_left = leftx_curr - win_len
        rect_x_right = leftx_curr + win_len

        # Find hot pixels in box and add to list of pixels
        good_left_inds = ((nonzeroy >= y_low) & (nonzeroy < y_high) &
                          (nonzerox >= rect_x_left) & (nonzerox < rect_x_right)).nonzero()[0]

        left_lane_inds.append(good_left_inds)

        # Update the x coordinate for the next box
        if len(good_left_inds) > minpix:
            leftx_curr = np.int(np.mean(nonzerox[good_left_inds]))

        # RIGHT WINDOW
        # Find the left and right x coordinate of the rect
        rect_x_left = rightx_curr - win_len
        rect_x_right = rightx_curr + win_len

        # Find hot pixels in box and add to list of pixels
        good_right_inds = ((nonzeroy >= y_low) & (nonzeroy < y_high) &
                          (nonzerox >= rect_x_left) & (nonzerox < rect_x_right)).nonzero()[0]

        right_lane_inds.append(good_right_inds)

        # Update the x coordinate for the next box
        if len(good_right_inds) > minpix:
            rightx_curr = np.int(np.mean(nonzerox[good_right_inds]))


    # Flatten indinces and fit a line
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    # VISUALIZATION
    ploty = np.linspace(0, image.shape[0] - 1, image.shape[0])

    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    cv2.fillPoly(out_image, np.int_([pts]), (153, 0, 76))

    return left_fit, right_fit, out_image
