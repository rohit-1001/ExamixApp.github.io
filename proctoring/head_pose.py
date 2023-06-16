import os
import cv2
import mediapipe as mp
import numpy as np
import threading as th
import sys
import cv2
import cvzone
import math
import dlib
from proctoring import detection
from backend.settings import BASE_DIR

# placeholders and global variables
x = 0  # X axis head pose
y = 0  # Y axis head pose

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# detector = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'haarcascade_frontalface_default.xml'))
# recognizer = cv2.face.LBPHFaceRecognizer_create()

X_AXIS_CHEAT = 0
Y_AXIS_CHEAT = 0

global flag
flag = True

predictor = dlib.shape_predictor(os.path.join(BASE_DIR, "shape_predictor_68_face_landmarks.dat"))
eye_tracker = None


def pose(stop_event, cheat_event, user_name, quiz_id):
    global VOLUME_NORM, x, y, X_AXIS_CHEAT, Y_AXIS_CHEAT, eye_tracker

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solutions

    while cap.isOpened():
        success, image = cap.read()

        # def frame_capture(count):
        #     if image is not None:
        #         # cv2.imwrite(BASE_DIR + '/Cheating/User.' + str(user_name) + "." + str(count) + ".jpg", image)
        #         # return image
        #         # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #         # faces = detector.detectMultiScale(gray, 1.3, 5)
        #         #
        #         # for (x, y, w, h) in faces:
        #         #     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #         #     count += 1
        #
        #         # Save the captured image into the datasets folder
        #         cv2.imwrite(BASE_DIR + '/Cheating/User.' + str(user_name) + "." + str(count) + ".jpg", image)
        #         print("Image saved")
        #
        #         if count == 5:
        #             cap.release()
        #
        #         return

        if detection.CHEAT_COUNT>10:
            detection.FINAL_CHEAT_COUNT+=1
            detection.CHEAT_COUNT=0
            # cam = cv2.VideoCapture(0)
            # ret, img = cam.read()
            # img = cv2.flip(img, -1) # flip video image vertically
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # faces = detector.detectMultiScale(gray, 1.3, 5)

            # for (x, y, w, h) in faces:
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # count += 1

            # Save the captured image into the datasets folder
            # cv2.imwrite(BASE_DIR + '/Cheating' +
            #              ".jpg", img)

            # cv2.imshow('Register Face', img)

            # k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            # if k == 27:
            #     break
            # elif count >= 30:  # Take 30 face sample and stop video
            #     break

            # cam.release()
            # cv2.destroyAllWindows()
            # print("Function called in headpose.pose")
            # head_pose.pose(stop_event, cheat_event, user_name).frame_capture(FINAL_CHEAT_COUNT)
            # print("Function returned from headpose.pose")
            # cv2.imwrite(BASE_DIR+'/Cheating/User.' + str(user_name) + '.' + str(FINAL_CHEAT_COUNT) + ".jpg", image)
            # image.save(BASE_DIR+'/Cheating/User.' + str(user_name) + '.' + str(FINAL_CHEAT_COUNT) + ".jpg")
            cv2.imwrite(BASE_DIR + '/Cheating/User.' + str(user_name) + "." +str(quiz_id) + "." + str(detection.FINAL_CHEAT_COUNT) + ".jpg", image)
            if detection.FINAL_CHEAT_COUNT>4 :
                print("cheat count=", detection.CHEAT_COUNT)

                cheat_event.set()
                stop_event.set()
                break
            print("CHEATING")

        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # Display the resulting frame
        # cv2.imshow('Video', image)

        # This is related to multiple face detection and the system exits if it occurs
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)

        ######################################################################################################
        count = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            count += 1
        if (count > 1):
            cv2.putText(image, str("Multiple faces detected."), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)
        ######################################################################################################

        # if len(faces) > 1:
        #     flag = False
        #     print("cheating supreme")
        #     sys.exit()

        # For tracking eye gazing
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect face landmarks
        results = face_mesh.process(frame_rgb)
        size = 0
        if results.multi_face_landmarks is not None:
            size = len(results.multi_face_landmarks)
        print("Size of results.multi_face_landmarks= ", size)
        if results.multi_face_landmarks:
            # get the first detected face landmarks
            landmarks = results.multi_face_landmarks[0]

            # get the positions of the left and right eye landmarks
            left_eye_pos = (
                int(landmarks.landmark[159].x * image.shape[1]),
                int(landmarks.landmark[159].y * image.shape[0])
            )
            right_eye_pos = (
                int(landmarks.landmark[386].x * image.shape[1]),
                int(landmarks.landmark[386].y * image.shape[0])
            )

            # draw circles around the left and right eyes
            cv2.circle(image, left_eye_pos, 5, (0, 255, 0), -1)
            cv2.circle(image, right_eye_pos, 5, (0, 255, 0), -1)

            # calculate the horizontal gaze angle
            horizontal_gaze_angle = math.atan2(right_eye_pos[1] - left_eye_pos[1], right_eye_pos[0] - left_eye_pos[0])

            # define angle thresholds for gaze directions
            right_angle_threshold = math.pi / 4+9
            left_angle_threshold = -math.pi / 4

            # compare the horizontal gaze angle with angle thresholds to determine gaze direction
            if horizontal_gaze_angle > right_angle_threshold:
                # print right direction
                cv2.putText(image, "Eye Direction : Right", (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif horizontal_gaze_angle < left_angle_threshold:
                # print left direction
                cv2.putText(image, "Eye Direction : Left", (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # print straight direction
                cv2.putText(image, "Eye Direction : Straight", (250, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # To improve performance
        image.flags.writeable = False

        # Get the result
        results = face_mesh.process(image)

        # To improve performance
        image.flags.writeable = True

        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        face_ids = [33, 263, 1, 61, 291, 199]

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None)

                for idx, lm in enumerate(face_landmarks.landmark):
                    # print(lm)
                    if idx in face_ids:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])

                        # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                # The Distance Matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                print(x)
                print(y)

                # See where the user's head tilting
                if y < -12:
                    text = "Looking Left"
                elif y > 12:
                    text = "Looking Right"
                elif x < -12:
                    text = "Looking Down"
                else:
                    text = "Forward"
                text = str(int(x)) + "::" + str(int(y)) + text
                # print(str(int(x)) + "::" + str(int(y)))
                # print("x: {x}   |   y: {y}  |   sound amplitude: {amp}".format(x=int(x), y=int(y), amp=audio.SOUND_AMPLITUDE))

                # Y is left / right
                # X is up / down
                if y < -12 or y > 12:
                    X_AXIS_CHEAT = 1
                else:
                    X_AXIS_CHEAT = 0

                if x < -12:
                    Y_AXIS_CHEAT = 1
                else:
                    Y_AXIS_CHEAT = 0

                # print(X_AXIS_CHEAT, Y_AXIS_CHEAT)
                # Display the nose direction
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))

                cv2.line(image, p1, p2, (255, 0, 0), 2)

                # Add the text on the image
                cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Head Pose Estimation', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
        if stop_event.is_set():
            # detection.CHEAT_COUNT = 0
            # detection.FINAL_CHEAT_COUNT = 0
            # detection.GLOBAL_CHEAT = 0
            # detection.PERCENTAGE_CHEAT = 0
            # detection.CHEAT_THRESH = 0.6
            # detection.XDATA = list(range(200))
            # detection.YDATA = [0] * 200
            print("Head pose thread closed.")
            # cap.release()
            break

    cap.release()


#############################
if __name__ == "__main__":
    t1 = th.Thread(target=pose)
    t1.start()
    t1.join()
