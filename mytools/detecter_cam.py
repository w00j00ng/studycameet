from scipy.spatial import distance as dist
from imutils import face_utils
import time
import dlib
import cv2
import cvlib as cv
from config import BASE_DIR
from studycam.views import cambot_views
import numpy as np
from keras.models import load_model


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


def is_eye_opened(detector, predictor, gray, lStart, lEnd, rStart, rEnd):
    EYE_AR_THRESH = 0.27
    rects = detector(gray, 0)
    if not rects:
        return -1
    rect = rects[0]
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)

    ear = (leftEAR + rightEAR) / 2.0  # average the eye aspect ratio together for both eyes
    # check to see if the eye aspect ratio is below the blink
    if ear < EYE_AR_THRESH:
        return 0
    return 1


def get_emotion(faces, gray, model):
    label_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}
    try:
        face = faces[0]
        (startX, startY) = face[0], face[1]
        (endX, endY) = face[2], face[3]
        face_crop = np.copy(gray[startY:endY, startX:endX])
        face_crop = cv2.resize(face_crop, (48, 48))
        face_crop = np.expand_dims(face_crop, axis=0)
        face_crop = face_crop.reshape((1, 48, 48, 1))
        result = model.predict(face_crop)
        result = list(result[0])
        if max(result) > 0.9:
            emotion_index = result.index(max(result))
            return label_dict[emotion_index]
    except IndexError:
        return "No Face"
    except cv2.error:
        return "No Face"
    return "No Emotion"


def main():
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

    emotion_model = load_model(f"{BASE_DIR}/mytools/model_optimal.h5")

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 내장 카메라 또는 외장 카메라에서 영상을 받아오기
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # capture.set(option, n), 카메라의 속성을 설정
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # option: 프레임의 너비와 높이등의 속성을 설정, n: 너비와 높이의 값을 의미

    emotion_data = {
        'Angry': 0,
        'Disgust': 0,
        'Fear': 0,
        'Happy': 0,
        'Neutral': 0,
        'Sad': 0,
        'Surprise': 0,
        'No Emotion': 0,
        'No Face': 0,
        'Total': 0
    }

    eye_data = {
        -1: 0,
        0: 0,
        1: 0
    }

    totalClosedTime = 0
    eyeClosedTime = 0

    report_count = 0
    loop_count = 0

    REPORT_DURATION = 10

    # start the video stream thread
    # print("[INFO] starting video stream thread...")
    # print("[INFO] print q to quit...")
    start_time = time.time()
    lastEyeOpenedTime = start_time
    FirstIter = True
    eyeClosed = False

    # loop over frames from the video stream
    while True:
        now_time = time.time()

        if now_time - start_time > REPORT_DURATION:
            report_data = {
                'report_count': report_count,
                'emotion_data': emotion_data,
                'eye_data': eye_data,
                'totalClosedTime': int(totalClosedTime),
                'loop_count': loop_count
            }
            cambot_views.upload(report_data)
            start_time = now_time
            report_count += 1

            emotion_data = dict.fromkeys(emotion_data, 0)
            eye_data = dict.fromkeys(eye_data, 0)
            loop_count = 0
            totalClosedTime = 0
            eyeClosedTime = 0

        ret, frame = capture.read()  # 카메라의 상태 및 프레임, ret은 카메라 상태 저장(정상 작동 True, 미작동 False)
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            continue

        faces, confidences = cv.detect_face(frame)

        present_emotion = get_emotion(faces, gray, emotion_model)
        present_eye = is_eye_opened(detector, predictor, gray, lStart, lEnd, rStart, rEnd)

        eyecheck_now = time.time()

        if FirstIter:
            first_time = eyecheck_now
            lastEyeOpenedTime = first_time
            totalClosedTime = 0
            eyeClosedTime = 0
            FirstIter = False
            eyeClosed = False

        if present_eye == 1:
            lastEyeOpenedTime = eyecheck_now
            totalClosedTime += eyeClosedTime
            eyeClosedTime = 0
            eyeClosed = False
        elif present_eye == 0:
            if eyeClosed:
                eyeClosedTime = eyecheck_now - lastEyeOpenedTime
            eyeClosed = True

        emotion_data[present_emotion] += 1
        loop_count += 1
        eye_data[present_eye] += 1

        cv2.putText(frame, "Press 'p' to Pause", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Press 'q' to Exit", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Study Cameet", frame)
        key = cv2.waitKey(33)

        if key == ord("p"):
            while True:
                key = cv2.waitKey(33)
                if key == ord("p"):
                    start_time = time.time()
                    break

        if key == ord("q"):  # if the `q` key was pressed, break from the loop
            cambot_views.commit_data()
            break

    capture.release()  # do a bit of cleanup
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
