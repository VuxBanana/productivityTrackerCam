import cv2
import numpy as np
import time

video = cv2.VideoCapture(0)  # Set up the webcam

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

face_present = False
face_start_time = None
no_face_start_time = None

total_face_duration = 0
total_no_face_duration = 0

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

while True:
    ret, frame = video.read()  # Read frame from the webcam

    # Apply face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=12, minSize=(100, 145)) #NIJE DOBRO NASTELOVANO, NASTELUJ!
    face_present = len(faces) > 0

    # Display the frame with rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    

    if face_present:
        if not face_start_time:
            # Face was not present in the previous frame, so it has just appeared
            face_start_time = time.time()
            if no_face_start_time:
                # Calculate the duration of no face presence and add to the total
                no_face_end_time = time.time()
                no_face_duration = no_face_end_time - no_face_start_time
                total_no_face_duration += no_face_duration
                no_face_start_time = None
    else:
        if face_start_time:
            # Face was present in the previous frame, but now it has disappeared
            face_end_time = time.time()
            face_duration = face_end_time - face_start_time
            total_face_duration += face_duration
            face_start_time = None
        if not no_face_start_time:
            # No face was not present in the previous frame, so it has just appeared
            no_face_start_time = time.time()

    cv2.imshow("Focus Tracker (Press 'Esc' to exit)", frame)  # Display the frame with face detection overlay

    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

# Release the webcam and close windows
video.release()
cv2.destroyAllWindows()



print("Productive time:", convert(total_face_duration))
print("Procrastination time:", convert(total_no_face_duration))
