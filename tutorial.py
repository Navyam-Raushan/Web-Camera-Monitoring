import cv2

# This array is a numpy array which reads the image(rgb matrices)
array = cv2.imread("myimage.png")

"""array.shape will give dimension of image matrix.
    (row, columns, color channels)
    (horizontol, vertical , numbers in an row
"""
print(array.shape)
print("With this matrix the image is created.")
print(array)
