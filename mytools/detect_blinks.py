from scipy.spatial import distance as dist
from imutils import face_utils
import time
import dlib
import cv2
import cvlib as cv
from config import BASE_DIR
from studycam.views import cambot_views


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


def main():
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 내장 카메라 또는 외장 카메라에서 영상을 받아오기
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # capture.set(option, n), 카메라의 속성을 설정
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # option: 프레임의 너비와 높이등의 속성을 설정, n: 너비와 높이의 값을 의미

    EYE_AR_THRESH = 0.27
    SLEEP_STD_TIME = 5
    bEyeOpened = True
    bSleep = False
    lastEyeClosedTime = 0

    SHAPE_PREDICTOR = f"{BASE_DIR}/mytools/shape_predictor_68_face_landmarks.dat"

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    # print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR)

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    # print("[INFO] starting video stream thread...")
    # print("[INFO] print q to quit...")

    # loop over frames from the video stream
    while True:
        now_time = time.time()
        ret, frame = capture.read()  # 카메라의 상태 및 프레임, ret은 카메라 상태 저장(정상 작동 True, 미작동 False)
        bbox, label, conf = cv.detect_common_objects(frame)

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            break
        try:
            if 'person' not in label:
                # print('Not in seat')
                continue
            if 'cell phone' in label or 'remote' in label:
                # print('cell phone')
                pass
            rect = detector(gray, 0)[0]  # detect faces in the grayscale frame
            print(rect)
            print(type(rect))
            cambot_views.working()

            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0  # average the eye aspect ratio together for both eyes

            # check to see if the eye aspect ratio is below the blink
            if ear < EYE_AR_THRESH:  # if eyes are closed
                if bEyeOpened:
                    lastEyeClosedTime = now_time
                else:
                    if lastEyeClosedTime > SLEEP_STD_TIME and not bSleep:
                        print("sleep")
                        bSleep = True
                bEyeOpened = False
            else:                    # if eyes are opened
                lastEyeClosedTime = now_time
                bEyeOpened = True
                bSleep = False

        except IndexError:  # when no face is detected
            print("Face is not straight")
            if lastEyeClosedTime - now_time > 5:
                lastEyeClosedTime = now_time

        cv2.putText(frame, "Press 'q' to Exit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Study Cameet", frame)
        key = cv2.waitKey(33)

        if key == ord("q"):  # if the `q` key was pressed, break from the loop
            break

    capture.release()  # do a bit of cleanup
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
