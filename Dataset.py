import cv2
import numpy as np
import os
import pickle

video = cv2.VideoCapture(0)  # Use the webcam to detect faces
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faces_data = []
i = 0
name = input("Enter your name:")


while True:
    ret, frame = video.read()  # Read from the webcam
    # camera filp code
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
    faces = facedetect.detectMultiScale(gray, 1.3, 5)  # Detect faces

    for (x, y, w, h) in faces:  # Loop through detected faces
        crop_img = frame[y:y + h, x:x + w, :]  # Crop the face from the image
        resized_img = cv2.resize(crop_img, (50, 50))  # Resize the face to 50x50 pixels

        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
        i = i + 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)  # Show the output frame
    k = cv2.waitKey(1)
    if len(faces_data) == 50:  # Stop after capturing 50 faces
        break

video.release()
cv2.destroyAllWindows()

# Save faces in pickle format

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(-1, 50*50*3)  # Flatten the images for the model (50*50 pixels * 3 color channels)

if not os.path.exists('data/'):
    os.makedirs('data/')

# Save or update the name list
if 'names.pkl' not in os.listdir('data/'):
    names = [name] * 50
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    names = names + [name] * 50
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

# Save or update face data
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    if faces.shape[1] != faces_data.shape[1]:
        print("Error: Dimension mismatch between existing and new data.")
    else:
        faces = np.append(faces, faces_data, axis=0)
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces, f)