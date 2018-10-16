# Standard package import:
import os
import time
import random
import win32gui
import win32con
import subprocess
from math import sin, cos, radians

# From packages import:
import cv2
import dlib
import xlrd
import pickle
import pyautogui
import numpy as np

# Directories declaration:
root_directory = os.path.dirname(os.path.abspath('__file__'))
binaries_directory = os.path.join(root_directory, 'Binaries\\')
cascades_directory = os.path.join(root_directory, 'Cascades\\')
excels_directory = os.path.join(root_directory, 'Excels\\')
faces_directory = os.path.join(root_directory, 'Faces\\')
if not os.path.exists(faces_directory):
    os.makedirs(faces_directory)
haar_directory = os.path.join(cascades_directory, 'Haar\\')
models_directory = os.path.join(root_directory, 'Models\\')
if not os.path.exists(models_directory):
    os.makedirs(models_directory)
screenshots_directory = os.path.join(binaries_directory, 'RemoteDesktopLogin\\terminal\\screenshots\\')

# Excel objects:
resource_details = xlrd.open_workbook(excels_directory + 'ResourceDetails.xlsx')
resource_data = resource_details.sheet_by_index(0)
resource_names = {}
for row_num in range(resource_data.nrows):
    resource_name_row = resource_data.row_values(row_num)
    resource_names[resource_name_row[0]] = resource_name_row[1]

# Recognizer declaration:
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Cascades object:
face_cascade = cv2.CascadeClassifier(haar_directory + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(haar_directory + 'haarcascade_eye.xml')
facial_landmarks_cascade = dlib.shape_predictor(cascades_directory + 'FacialLandmarksPredictor\\facial_landmarks.dat')

# Color variables:
red = [48, 59, 255]
blue = [255, 122, 0]
green = [100, 217, 76]
yellow = [0, 204, 255]
orange = [0, 149, 255]
teal_blue = [250, 200, 90]
purple = [214, 86, 88]
pink = [85, 45, 255]
white = [255, 255, 255]
black = [0, 0, 0]
color_array = [red, blue, green, yellow, orange, teal_blue, purple, pink, black]
hud_color = random.choice(color_array)

# Font variables:
font = cv2.FONT_HERSHEY_SIMPLEX
font_duplex = cv2.FONT_HERSHEY_DUPLEX

# Flag variables:
flag_variable = 0
ok_image = screenshots_directory + 'ok.PNG'

# Functions:
def face_hud(src, x, y, w, h, color):
    r = int(w / 20)
    adjustment = 0.15 * h
    h = int(h + adjustment)
    cv2.line(src, (x + r, y), (x + w - r, y), color)
    cv2.line(src, (x + r, y + h), (x + w - r, y + h), color)
    cv2.line(src, (x, y + r), (x, y + h - r), color)
    cv2.line(src, (x + w, y + r), (x + w, y + h - r), color)
    cv2.ellipse(src, (x + r, y + r), (r, r), 180, 0, 90, color)
    cv2.ellipse(src, (x + w - r, y + r), (r, r), 270, 0, 90, color)
    cv2.ellipse(src, (x + r, y + h - r), (r, r), 90, 0, 90, color)
    cv2.ellipse(src, (x + w - r, y + h - r), (r, r), 0, 0, 90, color)

def align_face(input_feed, angle):
    if angle == 0: return input_feed
    height, width = input_feed.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 0.9)
    result = cv2.warpAffine(input_feed, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def align_face_coords(pos, input_feed, angle):
    if angle == 0: return pos
    x = pos[0] - input_feed.shape[1] * 0.4
    y = pos[1] - input_feed.shape[0] * 0.4
    new_x = x * cos(radians(angle)) + y * sin(radians(angle)) + input_feed.shape[1] * 0.4
    new_y = -x * sin(radians(angle)) + y * cos(radians(angle)) + input_feed.shape[0] * 0.4
    return int(new_x), int(new_y), pos[2], pos[3]

def text_xy_pos(text):
    text_size = cv2.getTextSize(text, font, 0.5, 2)[0]
    text_x = (gray_feed.shape[1] - text_size[0]) / 2
    text_y = (gray_feed.shape[0] + text_size[1]) / 2
    return text_x, text_y

def click_on_visible(image, padding_x=0, padding_y=0, secs=0):
    image_button = None
    while image_button is None:
        image_button = pyautogui.locateOnScreen(image)
    image_button =  pyautogui.locateOnScreen(image)
    image_button_x, image_button_y = pyautogui.center(image_button)
    pyautogui.click(image_button_x + padding_x, image_button_y + padding_y)
    time.sleep(secs)

# Texts:
warning_text = 'TOO MANY PEOPLE IN THE VIEW!'
waiting_text = 'WAITING FOR FACE(S) TO BE DETECTED...'
face_detected_text = 'FACE DETECTED'
faces_detected_text = ' FACES DETECTED'
unfamiliar_face_text = 'UNFAMILIAR FACE(S) DETECTED!'

# Calling model and pickle file:
labels = {}
face_recognizer.read(models_directory + 'FaceModel.yml')
with open(models_directory + 'Faces.pickle', 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

# Output live feed:
live_capture = cv2.VideoCapture(0)

# Start FaceID:
while (True):
    ret, color_feed = live_capture.read()
    ratio = 300.0 / color_feed.shape[1]
    dimensions = (300, int(color_feed.shape[0] * ratio))
    gray_feed = cv2.cvtColor(color_feed, cv2.COLOR_BGR2GRAY)
    face_in_feed = face_cascade.detectMultiScale(gray_feed, scaleFactor=1.3, minNeighbors=5)

    if len(face_in_feed) == 1:
        for angle in [0, -30, 30]:
            tilted_face = align_face(gray_feed, angle)
            face_in_feed = face_cascade.detectMultiScale(tilted_face, scaleFactor=1.3, minNeighbors=5)
            if len(face_in_feed):
                face_in_feed = [align_face_coords(face_in_feed[-1], gray_feed, -angle)]
                break
 
    warning_pos = text_xy_pos(warning_text)
    waiting_pos = text_xy_pos(waiting_text)
    face_pos = text_xy_pos(face_detected_text)
    faces_pos = text_xy_pos(faces_detected_text)
    unfamiliar_pos = text_xy_pos(unfamiliar_face_text)

    if len(face_in_feed) == 0:
        cv2.rectangle(color_feed, (5, 5), (int(waiting_pos[0] * 2 + 30), int(waiting_pos[1] * 0.16) + 5), red, 1)
        cv2.rectangle(color_feed, (10, 10), (int(waiting_pos[0] * 2 + 25), int(waiting_pos[1] * 0.16)), black, -1)
        cv2.putText(color_feed, waiting_text, (15, 30), font, 0.5, white, 1, cv2.LINE_AA)
    elif len(face_in_feed) > 3:
        # Blurs the feed if more than 3 faces are detected:
        color_feed = cv2.GaussianBlur(color_feed, (25, 25), 3)
        cv2.rectangle(color_feed, (int(warning_pos[0]) - 15, int(warning_pos[1]) - 25), (int(warning_pos[0]) + (int(warning_pos[0] * 1.42) + 5), int(warning_pos[1]) + 15), white, 1)
        cv2.rectangle(color_feed, (int(warning_pos[0]) - 10, int(warning_pos[1]) - 20), (int(warning_pos[0]) + int(warning_pos[0] * 1.42), int(warning_pos[1]) + 10), black, -1)
        cv2.putText(color_feed, warning_text, (int(warning_pos[0]), int(warning_pos[1])), font_duplex, 0.5, red, 1, cv2.LINE_AA)
    else:
        # Facial Landmarks:
        for (x, y, w, h) in face_in_feed:
            if len(face_in_feed) == 1:
                face_hud(color_feed, x, y, w, h, yellow)
            elif len(face_in_feed) <= 3:
                face_hud(color_feed, x, y, w, h, random.sample(hud_color, 3))
            r = int(w / 20)
            face_detection_box = cv2.rectangle(color_feed, (x + r, y), (x + r, y), yellow, 1)
            face_detection_box_using_dlib = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
            detected_landmarks = facial_landmarks_cascade(color_feed, face_detection_box_using_dlib).parts()
            facial_landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])
            for idx, point in enumerate(facial_landmarks):
                position = (point[0, 0], point[0, 1])
                cv2.circle(color_feed, position, 0, white, -1)

            # Focusing on face:
            roi_gray_feed = gray_feed[y:y + h, x:x + w]
            roi_color_feed = color_feed[y:y + h, x:x + w]
            
            # ID = Name of the face; Confidence = Accuracy*
            ID, confidence = face_recognizer.predict(roi_gray_feed)
            identified = 'Matched : {}%'.format(str(round(confidence)))
            textsize = cv2.getTextSize(identified, font, 1, 2)[0]
            horizontal_alignment = (face_detection_box.shape[1] - textsize[0]) / 2

            # Confidence factor:
            if confidence >= 55 and confidence < 100:
                if len(face_in_feed) == 0:
                    pass
                elif len(face_in_feed) == 1:
                    cv2.rectangle(color_feed, (5, 5), (int(waiting_pos[0] - 10), int(waiting_pos[1] * 0.16) + 5), red, 1)
                    cv2.rectangle(color_feed, (10, 10), (int(waiting_pos[0] - 15), int(waiting_pos[1] * 0.16)), black, -1)
                    cv2.putText(color_feed, face_detected_text, (15, 30), font, 0.5, white, 1,  cv2.LINE_AA)
                    cv2.putText(face_detection_box, identified, (x + w + textsize[1] - 15, y - int(textsize[1] / 2)), font_duplex, 0.6, white, 1, cv2.LINE_AA)
                    cv2.line(color_feed, (x + w + 7, y), (x + w + 160, y), white)
                    cv2.putText(face_detection_box, labels[ID], (x + w + textsize[1] - 15, y + int(textsize[1] / 2) + 10), font, 0.5, white, 1, cv2.LINE_AA)

                    # Checking names off Excel file:
                    for row_num in range(resource_data.nrows):
                        row_value = resource_data.row_values(row_num)
                        if row_value[0] == labels[ID] and resource_names[row_value[0]] == 'no':
                            flag_variable = 1
                            cv2.putText(face_detection_box, row_value[4], (x + w + textsize[1] - 15, y + int(textsize[1] + 17)), font, 0.5, white, 1, cv2.LINE_AA)
                            os.startfile(faces_directory + labels[ID] + '\\Script\\' + labels[ID].lower() + '_rdp_login.ps1')
                            click_on_visible(ok_image, 5)
                            os.startfile(binaries_directory + 'RemoteDesktopLogin\\terminal\\LoginAssist.pyw')
                            resource_names[row_value[0]] = 'yes'
                            flag_variable = 0
                else:
                    cv2.putText(face_detection_box, labels[ID], (x, y + h + int(h * 0.15) + textsize[1]), font, 0.5, white, 1, cv2.LINE_AA)
                    cv2.rectangle(color_feed, (5, 5), (int(waiting_pos[0] + 17), int(waiting_pos[1] * 0.16) + 5), red, 1)
                    cv2.rectangle(color_feed, (10, 10), (int(waiting_pos[0] + 12), int(waiting_pos[1] * 0.16)), black, -1)
                    cv2.putText(color_feed, str(face_in_feed.shape[0]) + faces_detected_text, (15, 30), font, 0.5, white, 1, cv2.LINE_AA)
            else:
                cv2.rectangle(color_feed, (5, 5), (int(unfamiliar_pos[0] + 80), int(waiting_pos[1] * 0.16) + 5), white, 1)
                cv2.rectangle(color_feed, (10, 10), (int(unfamiliar_pos[0] + 75), int(waiting_pos[1] * 0.16)), black, -1)
                cv2.putText(color_feed, unfamiliar_face_text, (15, 30), font, 0.5, red, 1, cv2.LINE_AA)

    # Output window:
    resized_feed = cv2.resize(color_feed, dimensions, interpolation=cv2.INTER_AREA)
    cv2.imshow('XA Face ID - Live Output Feed', color_feed)
    if cv2.waitKey(5) & 0xFF == int(27):
        print('>>> Ending Live Output Feed...\n>>> Live Feed stopped.')
        break

# Releasing object:
live_capture.release()
cv2.destroyAllWindows()