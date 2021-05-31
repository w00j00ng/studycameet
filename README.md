# [스터디캠잇 기술 명세서]

#### 프레임워크

- 플라스크
- SQLite

#### 참여자

- 박예영 twoone67@naver.com
- 용우중 magoswj@gmail.com
- 윤선미 yunseonmi97@naver.com



## 1. 메뉴

#### (1) 공부하기

- 시작하기 버튼을 누르면 스터디캠이 실행됩니다
- 스터디캠이 실행되면 촬영된 학습자의 모습을 분석하여 데이터를 실행합니다
- 'q'를 누르면 스터디캠이 종료되고 그 동안 생성된 데이터가 데이터 베이스에 커밋됩니다

#### (2) 계정생성

- 회원구분, 아이디, 비밀번호, 이메일을 입력하고 생성하기 버튼을 누르면 회원가입을 할 수 있습니다.
- 회원구분은 학생과 강사로 구분됩니다. 한 계정에 학생과 강사를 중복할 수 없습니다.
- 아이디와 이메일은 다른 회원의 아이디, 이메일과 중복될 수 없습니다.

#### (3) 내 학습 데이터

- 수강한 수업에 대한 집중도, 자세, 날짜, 시간을 볼 수 있습니다
- 본인 개인의 데이터만 조회할 수 있습니다
- 학생이 뒤로가기를 이용하여 같은 부분을 중복해서 학습한 경우 데이터는 중복해서 발생합니다.

#### (4) 내 강의 데이터

- 본인 수업을 수강한 학생의집중도, 자세, 학생 수를 조회할 수 있습니다
- 수강한 모든 학생의 집계 정보를 표시하고, 학생 개별 정보는 조회할 수 없습니다

#### (5) 로그인/로그아웃

- 아이디 / 비밀번호를 입력하고 로그인합니다
- 비로그인 상태에서 메뉴는 공부하기, 계정생성, 로그인입니다
- 학생으로 로그인할 경우 내 학습 데이터 메뉴가 추가됩니다.
- 강사로 로그인할 경우 메뉴는 공부하기 메뉴가 사라지고, 내 강의 데이터 메뉴가 추가됩니다.
  - 강사는 공부하기 기능을 이용할 수 없습니다



## 2. 공부하기

![studycamlogic](https://github.com/w00j00ng/studycameet/blob/main/README/studycamlogic.png?raw=true)

#### (1) 이용방법

- 프로그램은 while 루프를 돌 때마다 화면을 캡쳐하면서 동작합니다

```python
while True:
    ret, frame = capture.read()
    #--------생략--------#
    cv2.imshow("Study Cameet", frame)
```

- 버튼을 눌러 프로그램을 제어할 수 있습니다
  - q: 종료 / p: 일시정지
  - k: 5초 앞으로 / l: 5초 뒤로
  - h: 배속을 0.2 줄임 (최소 배속 0.4) / j :  배속을 0.2 늘림 (최대 배속 2.0)

#### (2) 종료 / 일시정지 기능

- q를 누르면 데이터가 커밋되고 프로그램이 종료됩니다

```python
	key = cv2.waitKey(33)
    if key == ord("q"):
        cambot_views.commit_data()
        break
```

- p를 누르면 일시정지됩니다
  - 일시정지 상태에서 q를 누르면 데이터가 커밋되고 프로그램이 종료됩니다

```python
    key = cv2.waitKey(33)
    if key == ord("p"):
        quitChk = False
        while True:
            key = cv2.waitKey(33)
            if key == ord("p"):
                start_time = time.time()
                break
            if key == ord("q"):
                cambot_views.commit_data()
                quitChk = True
                break
        if quitChk:
            break
```

#### (3) 재생속도, 앞으로가기/뒤로가기 기능
- k, l를 누르면 5초 앞, 뒤로 갈 수 있습니다

  - 보고 시간을 조정하는 방법으로 구현했습니다
  - 키를 누르면 화면에 5초 앞으로가기/뒤로가기 문자가 잠깐 표시됩니다

  - k :  5초 앞으로 가기
  - l :  5초 뒤로 가기

```python
last_report_time = time.time()
part_time_modifier = 0

while True:
	now_time = time.time()
    part_time = now_time - last_report_time
    if part_time * play_speed + part_time_modifier > REPORT_DURATION:
        #--------생략--------#
        cambot_views.upload(report_data)
        #--------생략--------#
        last_report_time = now_time    
    #--------생략--------#
    key = cv2.waitKey(33)
    if key == ord("k"):
        cv2.putText(frame, "5 <<", (400, 435),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        part_time_modifier -= 5
        if part_time + part_time_modifier < 0:
            part_time_modifier += REPORT_DURATION
            part_number -= 1
            if part_number < 0:
                part_number = 0
    if key == ord("l"):
        cv2.putText(frame, ">> 5", (400, 435),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        part_time_modifier += 5
        if part_time + part_time_modifier > REPORT_DURATION:
            part_time_modifier -= REPORT_DURATION
            part_number += 1
```

- h, j를 누르면 강의 배속을 설정할 수 있습니다
  - 보고주기를 조절하는 방법으로 구현했습니다
  - h :  배속을 0.2 줄임 (최소 배속 0.4)
  - j :  배속을 0.2 늘림 (최대 배속 2.0)

```python
    if part_time * play_speed + part_time_modifier > REPORT_DURATION:
        #--------생략--------#
        cambot_views.upload(report_data)
        #--------생략--------#
        last_report_time = now_time
    
    ret, frame = capture.read()
    #--------생략--------#
    key = cv2.waitKey(33)
    #--------생략--------#
    if key == ord("h"):
        play_speed -= 0.2
        if play_speed < 0.4:
            play_speed = 0.4

    if key == ord("j"):
        play_speed += 0.2
        if play_speed > 2.0:
            play_speed = 2.0
```


#### (4) 눈 상태 분석

- dlib 모듈의 get_frontal_face_detector()을 통해 정면 얼굴을 감지합니다
- dlib 모듈의 shape_predictor()를 통해 감지된 얼굴의 각 요소를 추출합니다
- face_utils 모듈의 FACIAL_LANDMARKS_IDXS를 통해 얼굴에서 왼쪽 눈과 오른쪽 눈의 좌표를 추출합니다

```python
def main():   
    SHAPE_PREDICTOR = f"{BASE_DIR}/mytools/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR)
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
```

- 좌표의 유클라디안 거리를 통해 각 눈의 감긴 정도를 추출합니다
  - 눈의 세로 길이를 가로 길이로 나누어 감긴 정도를 수치화합니다

```python
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)
```

- 각 눈의 감긴 정도를 바탕으로 눈이 감겼는지 여부를 반환합니다
  - 눈을 뜨고 있다면 1을, 감고 있다면 0을 반환합니다
  - 정면 얼굴이 검출되지 않았다면 -1을 반환합니다

```python
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

    ear = (leftEAR + rightEAR) / 2.0
    if ear < EYE_AR_THRESH:
        return 0
    return 1
```

- 눈이 감겼는지 여부를 데이터에 반영합니다

```python
eye_data = {
        -1: 0,
        0: 0,
        1: 0
    }
#--------생략--------#
while True:
    #--------생략--------#
    present_eye = is_eye_opened(detector, predictor, gray, lStart, lEnd, rStart, rEnd)
    eye_data[present_eye] += 1
```

#### (5) 감정 분석

- cv 모듈의 detect_face() 메서드를 이용하여 얼굴을 검출합니다

```python
faces, confidences = cv.detect_face(frame)
```

- 검출된 얼굴의 좌표를 함수에 전달합니다

```python
def get_emotion(faces, gray, emotion_model)
```

- 이 함수는 좌표, 이미지, 모델을 활용하여 감정분석 결과를 반환합니다
  1. 전체 이미지 중 해당 좌표에 해당하는 부분을 배열로 구성합니다
  2. 배열을 모델에 맞는 (1, 48, 48, 1)로 모양를 조정합니다
  3. 모델이 가장 확률이 높다고 평가한 감정과 그 확률값을 반환받습니다
  4. 해당 확률이 90%를 넘는다면 해당 감정을 반환합니다
  5. 넘지 않는다면 "No Emotion"을 반환합니다
  6. 얼굴이 검출되지 않았다면 "No Face"를 반환합니다

```python
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
        return "No_Face"
    except cv2.error:
        return "No_Face"
    return "No_Emotion"
```

- 감정분석 결과를 데이터에 반영합니다

```python
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
#--------생략--------#
while True:
    #--------생략--------#
    present_emotion = get_emotion(faces, gray, emotion_model)
    #--------생략--------#
    emotion_data[present_emotion] += 1
```

#### (6) views 전송 데이터 형식

```json
{
    'report_count': 1, 
    'emotion_data': {
        'Angry': 20, 
        'Disgust': 0, 
        'Fear': 15, 
        'Happy': 0, 
        'Neutral': 25, 
        'Sad': 0, 
        'Surprise': 0, 
        'No_Emotion': 1, 
        'No_Face': 0, 
        'Total': 66
    }, 
    'eye_data': {
        -1: 21, 
        0: 4,
        1: 41
    }, 
    'loop_count': 66
}
```

- views 파일에는 위와 같은 형태로 데이터가 전달됩니다
- 'report_cout'는 이 보고가 해당 수업의 몇 번째 토막인지 나타냅니다.
  - 0부터 시작하므로 위의 데이터는 해당 수업의 2번째 토막 데이터입니다
- 'emotion_data': 해당 토막에서의 감정 정보를 나타냅니다
  - 해당 감정이라고 몇 번 분석되었는지를 나타냅니다
  - 'No Emotion'은 판단 결과의 예측 확률이 낮은 경우입니다
  - 'No Face'는 얼굴이 없었던 경우입니다
- 'eye_data': 해당 토막에서 눈 깜빡임 정보를 나타냅니다
  - -1은 얼굴이 정면을 향하지 않았을 때입니다
  - 0은 눈을 감았을 때입니다
  - 1은 눈을 떴을 때 입니다
- 'loop_count'는 해당 토막에서 몇 번 촬영되었는지를 나타냅니다

#### (7) 데이터 정제

```python
@bp.route('/upload/', methods=["POST"])
def upload(report):
    #--------생략--------#

    rate_posture, rate_concentrate = 0, 0
    rate_angry, rate_disgust, rate_fear, rate_happy, rate_sad = 0, 0, 0, 0, 0

    if g.user:
        student_id = session.get('user_id')
    rate_posture = (report['eye_data'][0] + report['eye_data'][1]) / report['loop_count']
    if (report['eye_data'][0] + report['eye_data'][1]) != 0:
        rate_concentrate = report['eye_data'][1] / (report['eye_data'][0] + report['eye_data'][1])
    if report['emotion_data']['Total'] != 0:
        rate_angry = report['emotion_data']['Angry'] / report['emotion_data']['Total']
        rate_disgust = report['emotion_data']['Disgust'] / report['emotion_data']['Total']
        rate_fear = report['emotion_data']['Fear'] / report['emotion_data']['Total']
        rate_happy = report['emotion_data']['Happy'] / report['emotion_data']['Total']
        rate_sad = report['emotion_data']['Sad'] / report['emotion_data']['Total']

    total_loop = report['loop_count']

    #--------생략--------#
    db.session.add(input_data)
    print("======================data added======================")

    return redirect(url_for('cambot.index'))
```

- 자세는 정면 얼굴이 검출된 횟수에서 전체 횟수를 나누어 도출합니다
- 집중도는 눈을 뜨고 있는 횟수에서 정면 얼굴이 검출된 횟수를 나누어 도출합니다
- 각 감정의 정도는 해당 감정이 측정된 횟수에서 전체 감정이 측정된 횟수를 나누어 도출합니다

#### (8) 데이터 업데이트

```python
input_data = StudyLog(lecture_id=lecture_id,
                      lecture_part=lecture_part,
                      teacher_id=teacher_id,
                      student_id=student_id,
                      rate_posture=rate_posture,
                      rate_concentrate=rate_concentrate,
                      rate_angry=rate_angry,
                      rate_disgust=rate_disgust,
                      rate_fear=rate_fear,
                      rate_happy=rate_happy,
                      rate_sad=rate_sad,
                      total_loop=total_loop,
                      create_date= dt.datetime.today(),
                      create_time=dt.datetime.now().hour
                     )
db.session.add(input_data)
```

- 정제된 데이터를 데이터베이스에 업데이트 합니다
- 강의번호, 강사번호, 학생번호, 날짜, 시간에 대한 정보를 같이 전달합니다



## 3. 데이터 모델링

#### (1) User 테이블

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    div = db.Column(db.String(1), nullable=False)
```

- username과 email은 반드시 입력해야 하며 중복될 수 없습니다
- div열을 통해 학생을 0, 강사를 1로 구분합니다



#### (2) Lecture 테이블

```python
class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    subject_number = db.Column(db.Integer, nullable=True)
```

- teacher_id는 User의 id를 상속받는 개념입니다
- 강의를 등록할 때 과목명(subject)을 반드시 입력해야 합니다



#### (3) StudyLog 테이블

```python
class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, nullable=True)
    lecture_part = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, nullable=True)
    student_id = db.Column(db.Integer, nullable=False)
    rate_posture = db.Column(db.Float, nullable=False)
    rate_concentrate = db.Column(db.Float, nullable=False)
    rate_angry = db.Column(db.Float, nullable=False)
    rate_disgust = db.Column(db.Float, nullable=False)
    rate_fear = db.Column(db.Float, nullable=False)
    rate_happy = db.Column(db.Float, nullable=False)
    rate_sad = db.Column(db.Float, nullable=False)
    total_loop = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.Date(), nullable=False)
    create_time = db.Column(db.Integer, nullable=False)
```

- 강의번호, 강의토막번호, 강사번호, 학생번호를 상속받습니다
- 학생의 자세와 집중도를 입력받습니다
- 학생의 감정정보를 입력받습니다
  - angry는 분노, disgust는 우울, happy는 행복, sad는 슬픔, 감정에 대한 정보를 담아냅니다
- 생성된 날짜와 시간을 저장합니다



## 4. 마이 데이터 조회

- 집중도와 자세를 구간화하여 등급을 나누고 결과를 출력합니다

```python
def get_grade(rate):
    if rate > 0.9:
        grade = "아주좋음"
    elif rate > 0.6:
        grade = "좋음"
    elif rate > 0.4:
        grade = "보통"
    elif rate > 0.2:
        grade = "나쁨"
    else:
        grade = "아주나쁨"
    return grade
```

#### (1) 강사

- SQL문
  - 강사는 평균으로 집계된 정보를 조회할 수 있고 학생 개별의 정보는 확인할 수 없습니다
  - 강의의 토막별 정보를 조회할 수 있습니다

```python
@bp.route('/by_lecture/')
def by_lecture():
    data = db.engine.execute(
        f"SELECT   lecture_id "
        f"       , lecture_part "
        f"       , AVG(posture) "
        f"       , AVG(concentrate) "
        f"       , AVG(angry) "
        f"       , AVG(disgust) "
        f"       , AVG(fear) "
        f"       , AVG(happy) "
        f"       , AVG(sad) "
        f"       , COUNT (distinct student_id) "
        f"FROM ( "
        f"         SELECT   student_id "
        f"                , lecture_id "
        f"                , lecture_part "
        f"                , AVG(rate_posture)     posture "
        f"                , AVG(rate_concentrate) concentrate "
        f"                , AVG(rate_angry)       angry "
        f"                , AVG(rate_disgust)     disgust "
        f"                , AVG(rate_fear)        fear "
        f"                , AVG(rate_happy)       happy "
        f"                , AVG(rate_sad)         sad "
        f"         FROM     study_log "
        f"         WHERE    teacher_id = {session.get('user_id')} "
        f"         GROUP BY student_id "
        f"                , lecture_id "
        f"                , lecture_part "
        f"     ) "
        f"GROUP BY lecture_id "
        f"       , lecture_part"
    )
    report = {}
    row_num = 0
    for row in data:
        if row[0] not in report:
            report[row[0]] = {}
        emotion_list = [row[4], row[5], row[6], row[7], row[8]]
        emotion_label = ['스트레스', '우울', '불안', '행복', '슬픔']
        emotion_rank = heapq.nlargest(2, range(len(emotion_list)), key=emotion_list.__getitem__)
        report[row[0]][row[1]] = {
            'rate_posture': row[2],
            'grade_posture': get_grade(row[2]),
            'rate_concentrate': row[3],
            'grade_concentrate': get_grade(row[3]),
            'max_emotion': emotion_label[emotion_rank[0]],
            'max_emotion_rate': emotion_list[emotion_rank[0]],
            'second_emotion': emotion_label[emotion_rank[1]],
            'second_emotion_rate': emotion_list[emotion_rank[1]],
            'student_count': row[9],
        }
        row_num += 1
    if row_num == 0:
        return render_template('teacher/empty.html')
    return render_template('teacher/by_lecture.html', report=report)
```

- 출력결과

![teacher_bylecture](https://github.com/w00j00ng/studycameet/blob/main/README/teacher_bylecture.png?raw=true)

#### (2) 학생

- SQL 문
  - 학생은 개별 정보를 조회할 수 있습니다
  - 강의/토막별, 날짜별, 요일별, 시간별 통계정보를 제공합니다
  - 감정 정보는 제공하지 않습니다
- 강의 / 토막별 정보

![student_report](https://github.com/w00j00ng/studycameet/blob/main/README/student_bylecture.png?raw=true)

```python
@bp.route('/by_lecture/')
def by_lecture():
    data = db.engine.execute(
        f"SELECT   lecture_id "
        f"       , lecture_part "
        f"       , AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , COUNT(*) "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY lecture_id "
        f"       , lecture_part "
        f"ORDER BY lecture_id "
        f"       , lecture_part "
    )

    report = {}
    row_num, posture_sum, concentrate_sum = 0, 0, 0
    for row in data:
        if row[0] not in report:
            report[row[0]] = {}
        report[row[0]][row[1]] = {
            'rate_concentrate': row[2],
            'grade_concentrate': get_grade(row[2]),
            'rate_posture': row[3],
            'grade_posture': get_grade(row[3]),
            'count': row[4]
        }
        posture_sum += row[2]
        concentrate_sum += row[3]
        row_num += 1
    if row_num == 0:
        return render_template('student/empty.html')
    avg_info = [
        get_grade(posture_sum / row_num),
        posture_sum / row_num,
        get_grade(concentrate_sum / row_num),
        concentrate_sum / row_num
    ]
    return render_template('student/by_lecture.html', report=report, avg_info=avg_info)
```

- 날짜별 정보

![student_bydate](https://github.com/w00j00ng/studycameet/blob/main/README/student_bydate.png?raw=true)

```python
@bp.route('/by_date/')
def by_date():
    data = db.engine.execute(
        f"SELECT   AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , create_date "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY create_date "
        f"ORDER BY create_date desc"
    )
    result = []
    for row in data:
        result.append({
            'grade_concentrate': get_grade(row[0]),
            'rate_concentrate': row[0],
            'grade_posture': get_grade(row[1]),
            'rate_posture': row[1],
            'create_date': row[2]
        })
    return render_template('student/by_date.html', result=result)
```

- 요일별 정보

![student_byweekday](https://github.com/w00j00ng/studycameet/blob/main/README/student_byweekday.png?raw=true)

```python
@bp.route('/by_week/')
def by_week():
    data = db.engine.execute(
        f"SELECT   AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , strftime('%w', create_date) "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY strftime('%w', create_date) "
        f"ORDER BY strftime('%w', create_date) "
    )
    week_name = {"0": "일요일", "1": "월요일", "2": "화요일", "3": "수요일", "4": "목요일", "5": "금요일", "6": "토요일"}
    report = []
    for row in data:
        report.append({
            'grade_concentrate': get_grade(row[0]),
            'rate_concentrate': row[0],
            'grade_posture': get_grade(row[1]),
            'rate_posture': row[1],
            'weekday': week_name[row[2]]
        })
    return render_template('student/by_week.html', report=report)
```

- 시간별 정보

![student_bytime](https://github.com/w00j00ng/studycameet/blob/main/README/student_bytime.png?raw=true)

```python
@bp.route('/by_time/')
def by_time():
    data = db.engine.execute(
        f"SELECT   AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , create_time "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY create_time "
        f"ORDER BY create_time "
    )
    report = []
    for row in data:
        report.append({
            'grade_concentrate': get_grade(row[0]),
            'rate_concentrate': row[0],
            'grade_posture': get_grade(row[1]),
            'rate_posture': row[1],
            'create_time': row[2]
        })
    return render_template('student/by_time.html', report=report)
```



## 5. 챗봇

#### (1) 플로우차트

![studycameet](https://github.com/w00j00ng/studycameet/blob/main/README/chatbot_flowchart.png?raw=true)



## 6. 딥러닝 모델링

#### (1) 눈 상태 분석

##### ◎  개요

- 출처
  https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/

- 활용 라이브러리
  opencv, imutils, dlib

- 얼굴 이미지를 분석하여 각 요소의 좌표값을 반환

##### ◎  일반적인 모델의 특징과 한계

- 눈을 인식하고 그 중 하얀 부분(흰자)이 사라지면 눈을 감은 것으로 인식하는 방법
- 눈 부분에서 하얀 색을 띈 좌표값을 모두 도출해야 하기 때문에 연산 부담이 큼
- 동공의 크기, 홍채의 색, 눈의 크기 차이에 대한 반영이 없어 신뢰도가 낮음

##### ◎  적용 모델의 특징과 장점

- 눈의 테두리에서 6개의 좌표 추출
- 6개 좌표를 통해 눈의 세로 길이, 가로 길이를 도출
- 세로 길이와 가로 길이의 비율에 따라 감긴 정도를 판단
- 동공의 크기, 홍채의 색에 구애받지 않고 결과를 도출할 수 있음
- 6개 좌표에 대한 연산을 수행하기 때문에 연산 부담이 적음

![img](https://github.com/w00j00ng/studycameet/blob/main/README/blink_detection_6_landmarks.jpg?raw=true)

![img](https://github.com/w00j00ng/studycameet/blob/main/README/blink_detection_equation.png?raw=true)

##### ◎  한계점

- 얼굴이 정면을 향해 있을 때만 연산 가능
- 얼굴이 측면을 향해 있을 때 얼굴 각 요소의 좌표값을 확보할 필요가 있음



#### (2) 감정 분석

- 방법론
  - 캐글 감정 분석 데이터셋 활용
    - https://www.kaggle.com/aayushmishra1512/emotion-detector
    - 트레이닝 이미지 18,072건, 테스트 이미지 1,266건 활용
  - 감정을 6개로 구분하고 각 사진에 레이블값 부여
    - angry, disgusted, fearful, happy, sad, neutral
  - 사진과 레이블값을 기준으로 학습시킴
  - 컨볼루션 레이어, 백스풀링 레이어 활용
    - 컨볼루션 레이어를 활용하여 지역적 특징 도출
    - 맥스풀링 레이어를 활용하여 동일 지역에서의 사소한 변화를 무시
- 선정이유
  - 화면의 세부적인 요소까지 연산을 하게 되면 프로그램 성능이 낮아질 우려가 있음
  - 지역적 특징을 활용한 연산을 통해 연산 부담을 줄임
- 학습방법
  - keras 딥러닝 라이브러리 활용
  - epoch: 60 / batch_size: 64 / lr = 0.001
- 발전 방향
  - 현재의 방법은 사진을 바로 학습시켜 결과를 예측하는 모형으로 얼굴 각 요소에 대한 고려가 없음
  - 얼굴에서 눈, 입, 코 등의 각 요소를 분석하여 감정을 도출하는 모델로 발전시킬 필요가 있음
- 모델

```sh
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 48, 48, 32)        320       
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 48, 48, 64)        18496     
_________________________________________________________________
batch_normalization (BatchNo (None, 48, 48, 64)        256       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 24, 24, 64)        0         
_________________________________________________________________
dropout (Dropout)            (None, 24, 24, 64)        0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 24, 24, 128)       204928    
_________________________________________________________________
batch_normalization_1 (Batch (None, 24, 24, 128)       512       
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 12, 12, 128)       0         
_________________________________________________________________
dropout_1 (Dropout)          (None, 12, 12, 128)       0         
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 12, 12, 512)       590336    
_________________________________________________________________
batch_normalization_2 (Batch (None, 12, 12, 512)       2048      
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 6, 6, 512)         0         
_________________________________________________________________
dropout_2 (Dropout)          (None, 6, 6, 512)         0         
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 6, 6, 512)         2359808   
_________________________________________________________________
batch_normalization_3 (Batch (None, 6, 6, 512)         2048      
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 3, 3, 512)         0         
_________________________________________________________________
dropout_3 (Dropout)          (None, 3, 3, 512)         0         
_________________________________________________________________
flatten (Flatten)            (None, 4608)              0         
_________________________________________________________________
dense (Dense)                (None, 256)               1179904   
_________________________________________________________________
batch_normalization_4 (Batch (None, 256)               1024      
_________________________________________________________________
dropout_4 (Dropout)          (None, 256)               0         
_________________________________________________________________
dense_1 (Dense)              (None, 512)               131584    
_________________________________________________________________
batch_normalization_5 (Batch (None, 512)               2048      
_________________________________________________________________
dropout_5 (Dropout)          (None, 512)               0         
_________________________________________________________________
dense_2 (Dense)              (None, 6)                 3078      
=================================================================
Total params: 4,496,390
Trainable params: 4,492,422
Non-trainable params: 3,968
_________________________________________________________________
```

