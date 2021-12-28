import cv2
import datetime


class Camera:

    def __init__(self, source, picture_width=600, picture_height=600, fps=30, detection_area=(0, 0, 100, 200)):
        self._video_capture = cv2.VideoCapture(source)
        self._detection_area = detection_area
        Camera.picture_width = picture_width
        Camera.picture_height = picture_height
        Camera.frames_per_seconds = fps

    # get camera width
    @property
    def picture_width(self):
        return self._video_capture.get(3)

    # set camera width
    @picture_width.setter
    def picture_width(self, picture_width):

        if picture_width <= 0:
            return

        self._video_capture.set(3, picture_width)

    # get camera height
    @property
    def picture_height(self):
        return self._video_capture.get(4)

    # set camera height
    @picture_height.setter
    def picture_height(self, picture_height):

        if picture_height <= 0:
            return

        self._video_capture.set(4, picture_height)

    # get fps camera
    @property
    def frames_per_seconds(self):
        return self._video_capture.get(5)

    # set fps camera
    @frames_per_seconds.setter
    def frames_per_seconds(self, frames_per_seconds):
        self._video_capture.set(5, frames_per_seconds)

    def get_frame(self):
        _, frame = self._video_capture.read()
        return frame

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


class PersonCounter:

    def __init__(self, classifier):
        self._detected_persons = 0
        self._classifier = classifier
        self._loggingtable = []

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
    def classifier(self):
        return self._classifier

    # set the classifier for the Person detection
    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    @property
    def loggingtable(self):
        return self._loggingtable

    @loggingtable.setter
    def loggingtable(self, count):
        x = str(datetime.datetime.now().time())
        y = str(datetime.datetime.now().date())
        self._loggingtable.append([str(count), x, y])

    def detec_person(self, faces, detected_faces, detection_area):

        offset_x, offset_y, offset_width, offset_height = detection_area
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
                self._loggingtable = self.detected_person - number_of_person_old


class FileHandler:

    @staticmethod
    def export_file(file_path, logging_table):

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
