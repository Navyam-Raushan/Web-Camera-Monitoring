import time

import cv2
import time

# First we need to start camera
"""0 : to start primary camera
   1 : to start secondary(attached camera)
"""
video = cv2.VideoCapture(0)
time.sleep(1)

# Videos are made up of images only
# time.sleep(gives 1 sec for first frame if it is in loop video created 1 fps)
"""1 fps means 1 frames per second means 1 frame is read
    at each second."""

while True:
    # It will read whole video.
    # check means either camera open or not
    # frame means the matrix of the image (numpy array)

    check, frames = video.read()
    cv2.imshow("My video", frames)
    #     To exit from while loop we uses a key (if key == q) exit.
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()

"""The exit part takes q from keyboard
    if user presses key the loop will terminate
    but until unless camera waits for 1 sec 
    and then work flawlessesly until q is pressed."""

"""These part is only for experiment purpose."""
# Let's create image from that frame
# cv2.imwrite("myimage.png", frames)
