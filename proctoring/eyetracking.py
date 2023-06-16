import cv2
import dlib
import numpy as np

# Initialize the video capture device and the face and landmark detectors
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    # Read a frame from the video capture device
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the face in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If a face is detected, detect the eyes in the face and calculate the position of the pupils
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        landmarks = predictor(gray, rect)
        left_eye = np.array([(landmarks.part(36).x + landmarks.part(39).x) // 2, (landmarks.part(36).y + landmarks.part(39).y) // 2])
        right_eye = np.array([(landmarks.part(42).x + landmarks.part(45).x) // 2, (landmarks.part(42).y + landmarks.part(45).y) // 2])
        pupil_left = np.array([(landmarks.part(37).x + landmarks.part(38).x) // 2, (landmarks.part(37).y + landmarks.part(38).y) // 2])
        pupil_right = np.array([(landmarks.part(43).x + landmarks.part(44).x) // 2, (landmarks.part(43).y + landmarks.part(44).y) // 2])
        cv2.circle(frame, tuple(left_eye), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_eye), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(pupil_left), 2, (0, 255, 0), -1)
        cv2.circle(frame, tuple(pupil_right), 2, (0, 255, 0), -1)

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()
