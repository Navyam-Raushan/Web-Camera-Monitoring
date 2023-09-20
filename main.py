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
    # convert this frames to gaussian grey frame.
    gray_frame = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    """GaussianBlur is blurring technique which decrease from 
        a center point (bell-shaped curve.)"""
    # Here we have (frame, blur_value, deviation
    gaussian_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    cv2.imshow("My video", gaussian_frame)

    #     To exit from while loop we uses a key (if key == q) exit.
    # Create a keyboard key and then on press of it exit.
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
