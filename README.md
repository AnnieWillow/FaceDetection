# Face Detection Attendance System

This project utilizes Python and OpenCV using PyCharm to create an automated student attendance system based on face recognition. It uses a webcam to recognize faces and match them with a pre-recorded dataset.

## Features
- **Data Registration**: Students provide their name and ID to create a training dataset.
- **Face Recognition**: Real-time attendance tracking via face recognition.
- **Voice Confirmation**: After a successful match, Press 'O' for attendence taken and a voice prompt says "Attendance taken" .
- **Quick Exit**: Press 'Q' to quickly exit the system.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AnnieWillow/FaceDetection.git

## Usage
1. Training Mode: Run Dataset.py to register student data by entering their name and ID.
   
   ```bash
   python Dataset.py
   
   + The system trains the model using the provided data.

3. Attendance Mode: Run AttendanceRecord.py to track attendance with face recognition.
   
   ```bash
   python AttendanceRecord.py

   
   + Press 'O' to record attendance when the system recognizes a student.
   + Press 'Q' to exit the system.
  
## Files

- Dataset.py: Script to collect training data (name, ID, and face images).
- AttendanceRecord.py: Runs the real-time face recognition for attendance.
- haarcascade_frontalface_default.xml: Pre-trained face detection model used by OpenCV for webcam processing.
- attendance.csv: Stores attendance records with up-to-date time and date format.
- CV project.png: Background image used in the application interface.

## Contributing
Feel free to fork and submit pull requests for improvements.

