# Creating database
# It captures images and stores them in datasets
# folder under the folder name of sub_data
import cv2
import datetime
import detection_classes as cp

webcam = cp.Camera(0)
person_counter = cp.PersonCounter('datasets/haarcascade_frontal_face.xml')
face_cascade = cv2.CascadeClassifier(person_counter.classifier)

# 1 = calibration mode | 2 = Eingangstür Personenzähler | 3 = Schaufenster mode
mode = 1
none_face_counter = 0
fac_counter = 0
detected_faces = []

while True:

    offset_x, offset_y, width_detection_area, height_detection_area = webcam.detection_area
    frame = webcam.get_frame()
    sub_frame = frame[offset_y:height_detection_area + offset_y, offset_x:width_detection_area + offset_x, :]
    gray = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 4)

    if len(faces) == 0:
        none_face_counter += 1
        fac_counter = 0
    else:
        fac_counter += 1
        none_face_counter = 0

    if none_face_counter == webcam.frames_per_seconds:
        none_face_counter = 0
        detected_faces = []

    for x, y, w, h in faces:
        x += offset_x
        y += offset_y
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if mode == 1:

        cv2.rectangle(frame, (offset_x, offset_y), (width_detection_area, height_detection_area), (0, 0, 255), 2)
        webcam.detection_area = (200, 100, 600, 600)


    elif mode == 2:
        if fac_counter >= webcam.frames_per_seconds:
            person_counter.detec_person(faces, detected_faces, webcam.detection_area)

    elif mode == 3:
        pass

    cv2.imshow('OpenCV', frame)

    # export the logging data
    if len(person_counter.loggingtable) >= 50:
        is_sucessful = cp.FileHandler.export_file(person_counter.loggingtable, file_path=r"C:\Temp\Test.csv")
        if is_sucessful:
            person_counter.loggingtable = []

    key = cv2.waitKey(10)
    if key == 27:
        break
