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

first_frame = None
while True:
    # It will read whole video.
    # check means either camera open or not
    # frame means the matrix of the image (numpy array)

    check, frame = video.read()
    # convert this frames to gaussian grey frame.
    # gray_frame will have current
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """GaussianBlur is blurring technique which decrease from 
        a center point (bell-shaped curve.)"""
    # Here we have (frame, blur_value, deviation)
    # It holds current frame in each iteration.
    curr_gaussian_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # We have to get delta frame (diff of current and previous frames)
    # We will hold first frame in this variable (first iteratn first_frame == None
    if first_frame is None:
        first_frame = curr_gaussian_frame

    delta_frame = cv2.absdiff(first_frame, curr_gaussian_frame)

    # filtered frames using threshold frames.
    # Try to keep surrounding black and new object white only.
    thresh_frames = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]

    # Higher the iteration more the processing, configurn is set to none.
    dil_frames = cv2.dilate(thresh_frames, None, iterations=2)
    # cv2.imshow("My video", dil_frames)

    # Now let us find all different object(countours) entered.
    countours, check = cv2.findContours(dil_frames, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

    # iterate through countours and calculate area of each and mark as rect.
    for r in countours:
        # The rect which have smaller areas skip it as its fake (pixels sq)
        """Play with these areas to get utmost result
           crucially you just blackout surrounding as
           much as possible."""

        if cv2.contourArea(contour=r) < 5000:
            continue

        #     mark the rect along remaining areas.
        x, y, w, h = cv2.boundingRect(r)
        # We want to show that rectangle also
        """Giving two corners of rectangle pt1, pt2
            This will make a rectangle around given frame."""
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0),
                      thickness=3)

    cv2.imshow("Video", frame)

    # To exit from while loop we uses a key (if key == q) exit.
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
