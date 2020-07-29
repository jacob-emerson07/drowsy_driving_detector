import cv2, sys, winsound, datetime, os

from fastai import *
from fastai.vision import *

# Notes:
#	- Return Data Format: [Start Date, Start Time, Length of Time, Times Alerted]

def track():

	start = datetime.datetime.now()

	sDate = start.strftime('%Y-%m-%d')
	sTime = start.strftime('%H:%M:%S')

	num_alerts = start_camera()

	drive_length = int((datetime.datetime.now() - start).total_seconds())

	return [sDate, sTime, drive_length, num_alerts]
    

def start_camera():
    
    model = load_learner(".")
    
    defaults.device = torch.device('cpu')    

    eyless_frames = 0

    alerts = 0

    img_counter = 0

    faceCascade = cv2.CascadeClassifier(r".\Data_Files\haarcascade_eye.xml")

    video_capture = cv2.VideoCapture(0)


    while True:
        eyes_open = list()
	    # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        k = cv2.waitKey(1)

        eyes = faceCascade.detectMultiScale(
	        gray,
	        scaleFactor=1.7,
	        minNeighbors=5,
	        minSize=(30, 30),
	        flags=cv2.CASCADE_SCALE_IMAGE
	    )

        if len(eyes) > 0:
                    for i in range(len(eyes)):
                            im = gray[eyes[i][1]:eyes[i][1]+eyes[i][3], eyes[i][0]:eyes[i][0]+eyes[i][2]]
                            cv2.imwrite("test.jpg", im)
                            pred_class,pred_idx,outputs = model.predict(open_image("test.jpg"))
                            eyes_open.append(pred_class.obj)

        print("Open" not in eyes_open)
        if len(eyes) == 0 or "Open" not in eyes_open:
            eyless_frames += 1
            if eyless_frames % 48 == 0:
                winsound.Beep(1000, 2000)
                alerts += 1
	    
        else:
            eyless_frames = 0

	    # Draw a rectangle around each eye
        if "Open" in eyes_open:
            for (x, y, w, h) in eyes:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	    # Display the resulting frame
        cv2.imshow('FaceDetection', frame)

        if k%256 == 27: #ESC Pressed
	        break
        elif k%256 == 32:
	        # SPACE pressed
	        img_name = "facedetect_webcam_{}.png".format(img_counter)
	        cv2.imwrite(img_name, frame)
	        print("{} written!".format(img_name))
	        img_counter += 1
	        

	# When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
   
    return alerts
