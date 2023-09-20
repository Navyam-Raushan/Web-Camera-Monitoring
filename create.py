import numpy as np
import cv2

# Make an arrays of matrices and from that create an image.
array = np.array(
    [[[255, 0, 0],
      [255, 255, 255],
      [255, 255, 255],
      [187, 41, 160]],

     [[255, 200, 255],
      [255, 255, 255],
      [255, 255, 255],
      [255, 0, 255]],

     [[25, 155, 155],
      [0, 0, 0],
      [47, 255, 173],
      [255, 255, 255]]]
)

image = cv2.imwrite("new_image.png",array)

