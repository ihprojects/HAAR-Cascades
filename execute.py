import detection_classes as dc
import cv2

# Bevor irgendeine Loop startet, bitte diese beiden Objekte erstellen
person_counter = dc.PersonDetector('datasets/haarcascade_frontal_face.xml')
main = dc.Main(person_counter)

# Dies Loop kontinuierlich starten mit dem frame
main.start_loop(frame,fps)

# Button Event Calibration ON:
person_counter.operation_mode =1

# Button Event Eingangstür Personen zählen ON:
person_counter.operation_mode = 2

# Button Event Schaufenster Leute detektieren ON:
person_counter.operation_mode =3

#Event Schieberegler für detection area:
person_counter.detection_area =(offsetx,offstY, width, height)

# Der Rest läuft intern





