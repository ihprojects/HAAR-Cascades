import cv2
import datetime


class PersonDetector:

    def __init__(self, cascade_classifier, detection_area=(0, 0, 100, 200)):
        self._detected_persons = 0
        self._detection_area = detection_area
        self._cascade_classifier = cv2.CascadeClassifier(cascade_classifier)
        self._logging_table = []
        self._operation_mode = 2

    # get the person detection area -> tuple (start x - value, start y -value, width, height)
    @property
    def detection_area(self):
        return self._detection_area

    # set the person detection area
    @detection_area.setter
    def detection_area(self, detection_area):

        if type(detection_area) != tuple or len(detection_area) != 4:
            return
        else:
            self._detection_area = detection_area

    @property
    def operation_mode(self):
        return self._operation_mode

    @operation_mode.setter
    def operation_mode(self, mode):

        if mode < 1 and mode > 3:
            return
        self._operation_mode = mode

        # get the detected persons

    @property
    def detected_person(self):
        return self._detected_persons

    # set the detected persons
    @detected_person.setter
    def detected_person(self, detected_person):
        self._detected_persons = detected_person

    # get the classifier for the Person detection
    @property
    def cascade_classifier(self):
        return self._cascade_classifier

    # set the classifier for the Person detection
    @cascade_classifier.setter
    def cascade_classifier(self, classifier):
        self._cascade_classifier = classifier

    @property
    def logging_table(self):
        return self._logging_table

    @logging_table.setter
    def logging_table(self, count):
        x = str(datetime.datetime.now().time())
        y = str(datetime.datetime.now().date())
        self._logging_table.append([str(count), x, y])

    def detec_person(self, faces, detected_faces):

        offset_x, offset_y, offset_width, offset_height = self.detection_area
        print(self.detection_area)
        number_of_person_old = self.detected_person

        for (x, y, w, h) in faces:
            diff_x = None
            diff_y = None

            if len(detected_faces) != 0:
                for (x_old, y_old) in detected_faces:
                    x_difference = abs(x_old - x);

                    if x_difference < 30:
                        diff_y = abs(y - y_old)
                        diff_x = abs(x - y_old)
                        break

            if diff_y == None and diff_x == None:
                diff_x = offset_width + 1
                diff_y = offset_height + 1

            if diff_x > offset_width // 3 and diff_y > offset_y:
                detected_faces += [(x, y)]
                self.detected_person += 1
                self.logging_table = self.detected_person - number_of_person_old

class Main:

    def __init__(self, person_counter):
        self._none_face_counter = 0
        self._face_counter = 0
        self._person_detector = person_counter
        self._detected_faces =[]

    def start_loop(self, frame, fps):

        offset_x, offset_y, width_detection_area, height_detection_area = self._person_detector.detection_area
        sub_frame = frame[offset_y:height_detection_area + offset_y, offset_x:width_detection_area + offset_x, :]
        gray = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
        faces = self._person_detector.cascade_classifier.detectMultiScale(gray, 1.5, 4)


        if len(faces) == 0:
            self._none_face_counter += 1
            self._face_counter = 0
        else:
            self._face_counter += 1
            none_face_counter = 0

        if self._none_face_counter == fps:
            none_face_counter = 0
            self._detected_faces = []

        for x, y, w, h in faces:
            x += offset_x
            y += offset_y
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if self._person_detector.operation_mode == 1:
            cv2.rectangle(frame, (offset_x, offset_y), (width_detection_area, height_detection_area), (0, 0, 255), 2)

        elif self._person_detector.operation_mode == 2:
            if self._face_counter >= fps:
                self._person_detector.detec_person(faces, self._detected_faces)

        elif self._person_detector.operation_mode == 3:
            pass

        # export the logging data
        if len(self._person_detector.logging_table) >= 50:
            is_successful = FileHandler.create_csv(self._person_detector.logging_table, file_path=r"C:\Temp\Test.csv")
            if is_successful:
                self._person_detector.logging_table = []

        return frame




class FileHandler:

    @staticmethod
    def create_csv(file_path, logging_table):

        try:
            file = open(file_path, "a")
            for row in logging_table:
                for i, column in enumerate(row):
                    if i < 2:
                        file.write(f"{column}\t")
                    else:
                        file.write(f"{column}\n")
            file.close()
            return True

        except:
            return False
