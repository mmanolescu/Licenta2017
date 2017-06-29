
import cv2
import numpy as np

# image is expected be in RGB color space
def select_rgb_white_yellow(image):
    # white color mask
    thres = 50
    lower = np.uint8([thres, thres, thres])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)

    '''
    # yellow color mask
    lower = np.uint8([190, 190,   0])
    upper = np.uint8([255, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)

    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    '''

    masked = cv2.bitwise_and(image, image, mask = white_mask)

    return masked
