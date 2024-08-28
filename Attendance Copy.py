from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch


def speak(text):
    speak = Dispatch(('SAPI.SpVoice'))
    speak.Speak(text)


video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)
with open('data/ids.pkl', 'rb') as f:
    IDS = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)
print('Number of labels: ', len(LABELS))
print('Number of IDs: ', len(IDS))

# Ensure the number of labels, IDs, and faces match
if len(LABELS) != FACES.shape[0] or len(IDS) != FACES.shape[0]:
    raise ValueError("Mismatch in the number of faces, labels, or IDs.")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("CV project.png")

COL_NAMES = ['NAME', 'ID', 'TIME']

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    frame = cv2.flip(frame, 1)  # Camera flip

    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        # Get the index of the predicted label
        label_index = LABELS.index(output[0])
        predicted_id = IDS[label_index]

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        file_path = f"Attendance/Attendance_{date}.csv"
        exist: bool = os.path.isfile(file_path)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Add the ID to the attendance record
        attendance = [str(output[0]), str(predicted_id), str(timestamp)]

    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)
    if k == ord('o'):  # Press 'o' to record attendance
        speak("Attendance Taken..")
        time.sleep(5)
        with open(file_path, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(COL_NAMES)  # Write header if file does not exist
            writer.writerow(attendance)  # Write attendance record
    elif k == ord('q'):  # Press 'q' to exit
        break

video.release()
cv2.destroyAllWindows()
