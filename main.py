import cv2
from datetime import datetime
import streamlit as st
import time
import os
import glob
from emailing import send_mail
from threading import Thread


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


st.title("Motion Detector")
start = st.button("Start Camera")
# First we need to start camera
# """0 : to start primary camera
#    1 : to start secondary(attached camera)
# """
st.info("Please press stop button after few seconds.")
stop_button = st.button("Stop Camera")

if start:
    streamlit_img = st.image([])
    camera = cv2.VideoCapture(0)
    time.sleep(1)

    # Videos are made up of images only
    # time.sleep(gives 1 sec for first frame if it is in loop video created 1 fps)
    # """1 fps means 1 frames per second means 1 frame is read
    #     at each second."""

    #  We need 1,0 in last of the list then only we will send mail, pt of exit.
    count = 1
    status_list = []
    first_frame = None
    while True:
        now = datetime.now()

        status = 0
        # It will read whole video.
        # check means either camera open or not
        # frame means the matrix of the image (numpy array)

        check, frame = camera.read()
        # convert this frames to gaussian grey frame.
        # gray_frame will have current
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # """GaussianBlur is blurring technique which decrease from
        #     a center point (bell-shaped curve.)"""
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
            # """Play with these areas to get utmost result
            #    crucially you just blackout surrounding as
            #    much as possible."""

            if cv2.contourArea(contour=r) < 5000:
                continue

            #     mark the rect along remaining areas.
            x, y, w, h = cv2.boundingRect(r)
            # We want to show that rectangle also
            # """Giving two corners of rectangle pt1, pt2
            #     This will make a rectangle around given frame."""
            rectangle = cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0),
                                      thickness=3)
            if rectangle.any():
                status = 1
                cv2.imwrite(filename=f"images/{count}.png", img=frame)
                count = count + 1
                all_images = glob.glob("images/*.png")

                # chhosing mid image
                index = int(len(all_images) / 2)
                mid_image = all_images[index]

        status_list.append(status)
        status_list = status_list[-2:]
        # print(status_list)

        # LOGIC TO SEND MAIL
        if status_list[0] == 1 and status_list[1] == 0:
            # Args must be a tuple otherwise it will produce error.
            email_thread = Thread(target=send_mail, args=(mid_image, ))
            email_thread.daemon = True
            clean_thread = Thread(target=clean_folder)
            clean_thread.daemon = True

            # STARTING THE THREADS
            email_thread.start()
            clean_thread.start()
        # When we get the rect set status to 1
        # """so the idea is when object is just exit
        #    status will change 1 to 0 then we have to send a mail."""

        # LOGIC FOR TIMESTAMP
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(img=frame, org=(30, 30), text=now.strftime("%A"),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(150, 35, 170), thickness=1,
                    lineType=cv2.LINE_AA)

        cv2.putText(img=frame, org=(30, 60), text=now.strftime("%H:%M:%S"),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(150, 35, 170), thickness=1,
                    lineType=cv2.LINE_AA)
        streamlit_img.image(frame)

        # To exit from while loop we uses a key (if key == q) exit.
        # Create a keyboard key and then on press of it exit.
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if stop_button:
            camera.release()
            break



# """The exit part takes q from keyboard
#     if user presses key the loop will terminate
#     but until unless camera waits for 1 sec
#     and then work flawlessesly until q is pressed."""

# """These part is only for experiment purpose."""
# Let's create image from that frame
# cv2.imwrite("myimage.png", frames)
