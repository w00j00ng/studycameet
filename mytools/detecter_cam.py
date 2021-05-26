from scipy.spatial import distance as dist
from imutils import face_utils
import time
from time import strftime, gmtime
import dlib
import cv2
import cvlib as cv
from config import BASE_DIR
from studycam.views import cambot_views
import numpy as np
from keras.models import load_model


def eye_aspect_ratio(eye):
    left_vertical = dist.euclidean(eye[1], eye[5])
    right_vertical = dist.euclidean(eye[2], eye[4])
    horizontal = dist.euclidean(eye[0], eye[3])
    return (left_vertical + right_vertical) / (2.0 * horizontal)


def is_eye_opened(detector, predictor, gray, lStart, lEnd, rStart, rEnd):
    EYE_AR_THRESH = 0.27
    rects = detector(gray, 0)
    if not rects:
        return -1
    rect = rects[0]
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    left_eye = shape[lStart:lEnd]
    right_eye = shape[rStart:rEnd]
    left_EAR = eye_aspect_ratio(left_eye)
    right_EAR = eye_aspect_ratio(right_eye)

    ear = (left_EAR + right_EAR) / 2.0
    if ear < EYE_AR_THRESH:
        return 0
    return 1


def get_emotion(faces, gray, model):
    label_dict = { 0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise' }
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
        return "No_Face"
    except cv2.error:
        return "No_Face"
    return "No_Emotion"


def main():
    SHAPE_PREDICTOR = f"{BASE_DIR}/mytools/shape_predictor_68_face_landmarks.dat"

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    emotion_model = load_model(f"{BASE_DIR}/mytools/model_optimal.h5")

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    emotion_data = {
        'Angry': 0,
        'Disgust': 0,
        'Fear': 0,
        'Happy': 0,
        'Neutral': 0,
        'Sad': 0,
        'Surprise': 0,
        'No_Emotion': 0,
        'No_Face': 0,
        'Total': 0
    }

    eye_data = {
        -1: 0,
        0: 0,
        1: 0
    }

    part_number = 0
    loop_count = 0

    REPORT_DURATION = 20
    play_speed = 1

    last_report_time = time.time()

    b_first_iter = True
    start_time = 0
    operation_time_modifier = 0
    part_time_modifier = 0

    while True:
        now_time = time.time()
        if b_first_iter:
            start_time = now_time
            b_first_iter = False
        operation_time = now_time - start_time

        part_time = now_time - last_report_time

        if part_time * play_speed + part_time_modifier > REPORT_DURATION:
            report_data = {
                'part_number': part_number,
                'emotion_data': emotion_data,
                'eye_data': eye_data,
                'loop_count': loop_count
            }
            cambot_views.upload(report_data)
            last_report_time = now_time
            part_number += 1

            emotion_data = dict.fromkeys(emotion_data, 0)
            eye_data = dict.fromkeys(eye_data, 0)
            loop_count = 0

        ret, frame = capture.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            continue

        faces, confidences = cv.detect_face(frame)

        for face in faces:
            (startX, startY) = face[0], face[1]  # 시작위치 설정
            (endX, endY) = face[2], face[3]  # 종료위치 설정
            # draw rectangle over face
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)  # 박스 그리기

        present_emotion = get_emotion(faces, gray, emotion_model)
        present_eye = is_eye_opened(detector, predictor, gray, lStart, lEnd, rStart, rEnd)

        emotion_data[present_emotion] += 1
        emotion_data['Total'] += 1
        loop_count += 1
        eye_data[present_eye] += 1

        posture_status = "Good"
        concentrate_status = "Good"

        if present_emotion == 'No_Face' or present_eye == -1:
            posture_status = "Bad"
            concentrate_status = "Bad"
        elif present_eye == 0:
            concentrate_status = "Bad"

        cv2.putText(frame, "Press 'p' to Pause", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Press 'q' to Exit", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Posture: {posture_status}", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Concentrate: {concentrate_status}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Emotion: {present_emotion}", (10, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "k << Move 5 Seconds >> l", (10, 435),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "h << Config Play Speed >> j", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if play_speed < 0.9 or play_speed > 1.1:
            cv2.putText(frame, f"Play Speed x{round(play_speed, 1)}", (450, 460),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Part {part_number}", (450, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Now at {strftime('%M:%S', gmtime(int(part_number * REPORT_DURATION + part_time * play_speed + part_time_modifier)))}", (450, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Report in {round(REPORT_DURATION - (part_time * play_speed + part_time_modifier), 1)}", (450, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        key = cv2.waitKey(33)

        if key == ord("p"):
            quit_chk = False
            while True:
                key = cv2.waitKey(33)
                if key == ord("p"):
                    last_report_time = time.time()
                    break
                if key == ord("q"):
                    cambot_views.commit_data()
                    quit_chk = True
                    break
            if quit_chk:
                break

        if key == ord("k"):
            cv2.putText(frame, "5 <<", (400, 435),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            operation_time_modifier -= 5
            part_time_modifier -= 5
            if part_time + part_time_modifier < 0:
                part_time_modifier += REPORT_DURATION
                part_number -= 1

        if key == ord("l"):
            cv2.putText(frame, ">> 5", (400, 435),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            operation_time_modifier += 5
            part_time_modifier += 5
            if part_time + part_time_modifier > REPORT_DURATION:
                part_time_modifier -= REPORT_DURATION
                part_number += 1

        if key == ord("h"):
            play_speed -= 0.2
            if play_speed < 0.4:
                play_speed = 0.4

        if key == ord("j"):
            play_speed += 0.2
            if play_speed > 2.0:
                play_speed = 2.0

        if key == ord("q"):  # if the `q` key was pressed, break from the loop
            cambot_views.commit_data()
            break

        cv2.imshow("Studycameet", frame)

    capture.release()  # do a bit of cleanup
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
