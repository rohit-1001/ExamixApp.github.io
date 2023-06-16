import cv2
import mediapipe as mp
import math
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# initialize face mesh solution
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

while True:
    # read frame from camera
    ret, frame = cap.read()

    # convert frame to RGB color space
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect face landmarks
    results = face_mesh.process(frame_rgb)
    if results.multi_face_landmarks:
        # get the first detected face landmarks
        landmarks = results.multi_face_landmarks[0]

        # get the positions of the left and right eye landmarks
        left_eye_pos = (
            int(landmarks.landmark[159].x * frame.shape[1]),
            int(landmarks.landmark[159].y * frame.shape[0])
        )
        right_eye_pos = (
            int(landmarks.landmark[386].x * frame.shape[1]),
            int(landmarks.landmark[386].y * frame.shape[0])
        )

        # draw circles around the left and right eyes
        cv2.circle(frame, left_eye_pos, 5, (0, 255, 0), -1)
        cv2.circle(frame, right_eye_pos, 5, (0, 255, 0), -1)

        eye_gaze_x = landmarks.landmark[159].x - landmarks.landmark[386].x
        eye_gaze_y = landmarks.landmark[159].y - landmarks.landmark[386].y

        eye_midpoint = ((left_eye_pos[0] + right_eye_pos[0]) // 2, (left_eye_pos[1] + right_eye_pos[1]) // 2)

        # calculate the horizontal gaze angle
        horizontal_gaze_angle = math.atan2(right_eye_pos[1] - left_eye_pos[1], right_eye_pos[0] - left_eye_pos[0])

        # define angle thresholds for gaze directions
        right_angle_threshold = math.pi / 4
        left_angle_threshold = -math.pi / 4

        # compare the horizontal gaze angle with angle thresholds to determine gaze direction
        if horizontal_gaze_angle > right_angle_threshold:
            # print right direction
            cv2.putText(frame, "Right", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif horizontal_gaze_angle < left_angle_threshold:
            # print left direction
            cv2.putText(frame, "Left", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # print straight direction
            cv2.putText(frame, "Straight", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # show the frame
    cv2.imshow('Eye Tracking', frame)

    # exit if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# release resources
cap.release()
cv2.destroyAllWindows()
