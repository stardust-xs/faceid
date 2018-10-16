# Standard import:
import os
import sys
import time
import shutil
import base64
from tkinter import *
from tkinter import StringVar
from tkinter import messagebox
from math import sin, cos, radians

# Downloaded packages import:
import cv2
import dlib
import pickle
import PIL.Image
import numpy as np
from openpyxl import *
from colorama import init
from termcolor import colored
from PIL import Image, ImageTk

init()

# Directories declaration:
root_directory = os.path.dirname(os.path.abspath(__file__))
binaries_directory = os.path.join(root_directory, 'Binaries\\')
cascades_directory = os.path.join(root_directory, 'Cascades\\')
excels_directory = os.path.join(root_directory, 'Excels\\')
faces_directory = os.path.join(root_directory, 'Faces\\')
if not os.path.exists(faces_directory):
    os.makedirs(faces_directory)
haar_directory = os.path.join(cascades_directory, 'Haar\\')
images_directory = os.path.join(root_directory, 'Images\\')
models_directory = os.path.join(root_directory, 'Models\\')
if not os.path.exists(models_directory):
    os.makedirs(models_directory)

# Excel objects:
resource_details = load_workbook(excels_directory + 'ResourceDetails.xlsx')
resource_data = resource_details['Resource_Data']

# RDP object:
rdp_login_script = (binaries_directory + 'RemoteDesktopLogin\\config\\rdp_auto_login.ps1')

# Tkinter window object:
base_window = Tk()

# Cascades object:
face_cascade = cv2.CascadeClassifier(haar_directory + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(haar_directory + 'haarcascade_eye.xml')
facial_landmarks_cascade = dlib.shape_predictor(cascades_directory + 'FacialLandmarksPredictor\\facial_landmarks.dat')

# Color variables:
red = [0, 0, 255]
blue = [255, 0, 0]
green = [0, 255, 0]
yellow = [0, 255, 255]
orange = [31, 153, 232]
light_blue = [232, 153, 31]
white = [255, 255, 255]
black = [0, 0, 0]

# Font variables:
font = cv2.FONT_HERSHEY_SIMPLEX
font_duplex = cv2.FONT_HERSHEY_DUPLEX

# Variables:
filename = 1
last_empty_row = resource_data.max_row + 1

# Texts:
warning_text = 'MORE THAN ONE PERSON IN THE VIEW'
waiting_text = 'WAITING FOR A FACE TO BE DETECTED...'
face_capture_started = 'FACE CAPTURE STARTED...'

# GUI window:
# The below function is a Tkinter window which will act as the base window for the setup. The window is centered in the screen.
def window(main):
    main.title('XA FaceID')
    main.resizable(0, 0)
    main.update_idletasks()
    width = 325
    height = 318
    win_x = (main.winfo_screenwidth() // 2) - (width // 2)
    win_y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, win_x, win_y))
    main.iconbitmap(images_directory + 'xa_logo.ico')
window(base_window)

# New profile:
# The below function is used for creating new profiles which will be later used for identification. While setting up all fields
# are made mandatory for avoiding any errors.
def create_new_profile():
    global faces_directory
    global new_folder_path
    global new_folder_value
    global rdp_environment_value
    global rdp_user_id_value
    global rdp_password_value
    global enterprise_id_value
    faces_directory = os.path.join(root_directory, 'Faces\\')
    new_folder_value = input_folder_name.get()
    rdp_user_id_value = rdp_user_id.get()
    rdp_password_value = rdp_password.get()

    if len(input_folder_name.get()) == 0:
        messagebox.showwarning('Error', 'Please enter folder name.')
        sys.exit()
    elif len(input_folder_name.get()) > 16:
        messagebox.showwarning('Error', 'Maximum 15 characters are allowed.')
    elif len(input_folder_name.get()) <= 15:
        allowed_characters = set('0123456789_abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if set(input_folder_name.get()).issubset(allowed_characters):
            for search_row in resource_data.rows:
                if search_row[0].value == input_folder_name.get():
                    messagebox.showinfo('Warning', 'Name already exists. Please choose another name.')
                    cancel_window()
                else:
                    new_folder_path = faces_directory + input_folder_name.get() + '\\'
                    if not os.path.exists(new_folder_path):
                        created_folder = os.makedirs(new_folder_path)
                        username_cell = resource_data['A' + str(last_empty_row)]
                        username_cell.value = input_folder_name.get()
                        flag_cell = resource_data['B' + str(last_empty_row)]
                        flag_cell.value = 'no'
                        resource_details.save(excels_directory + 'ResourceDetails.xlsx')
        else:
            messagebox.showwarning('Error', 'Folder name cannot contain special characters.')

    if len(enterprise_id.get()) == 0:
        messagebox.showwarning('Error', 'Please enter Enterprise ID.')
        sys.exit()
    elif len(enterprise_id.get()) > 32:
        messagebox.showwarning('Error', 'Maximum 15 characters are allowed.')
    elif len(enterprise_id.get()) <= 31:
        allowed_characters = set('0123456789abcdefghijklmnopqrstuvwxyz.')
        if set(enterprise_id.get()).issubset(allowed_characters):
            enterprise_id_cell = resource_data['E' + str(last_empty_row)]
            enterprise_id_cell.value = enterprise_id.get()
            resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
        else:
            messagebox.showwarning('Error', 'Enterprise ID cannot contain special characters.')

    rdp_environment_cell = resource_data['C' + str(last_empty_row)]
    if rdp_environment_variable.get() == 1:
        rdp_environment_cell.value = 'BBP\\RMGP'
        rdp_environment_value = 'BBP\\RMGP'
        resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
    elif rdp_environment_variable.get() == 2:
        rdp_environment_cell.value = 'PREPROD\\RMGV'
        rdp_environment_value = 'PREPROD\\RMGV'
        resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
    elif rdp_environment_variable.get() == 3:
        rdp_environment_cell.value = 'TEST\\RMGN'
        rdp_environment_value = 'TEST\\RMGN'
        resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
    elif rdp_environment_variable.get() == 4:
        rdp_environment_cell.value = 'DEV\\RMGN'
        rdp_environment_value = 'DEV\\RMGN'
        resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
    else:
        rdp_environment_cell.value = 'TEST\\RMGN'
        rdp_environment_value = 'TEST\\RMGN'
        resource_details.save(excels_directory + '\\ResourceDetails.xlsx')

    if len(rdp_user_id.get()) == 0:
        messagebox.showwarning('Error', 'Please enter Terminal User ID.')
    elif len(rdp_user_id.get()) > 50:
        messagebox.showwarning('Error', 'Maximum 30 characters are allowed.')
    elif len(rdp_user_id.get()) <= 49:
        allowed_characters = set('0123456789_abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ\\/.')
        if set(rdp_user_id.get()).issubset(allowed_characters):
            rdp_user_id_cell = resource_data['D' + str(last_empty_row)]
            rdp_user_id_cell.value = rdp_user_id.get()
            resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
        else:
            messagebox.showwarning('Error', 'Invalid User ID.')

    if len(rdp_password.get()) == 0:
        messagebox.showwarning('Error', 'Please enter Terminal Password.')
    elif len(rdp_password.get()) > 21:
        messagebox.showwarning('Error', 'Password cannot contain more than 20 characters.')
    elif len(rdp_password.get()) <= 20:
        allowed_characters = set('0123456789_abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ\\.!@#$%^&*()-;<>?|/')
        if set(rdp_password.get()).issubset(allowed_characters):
            rdp_password_cell = resource_data['XA' + str(last_empty_row)]
            rdp_password_cell.value = rdp_password.get()
            resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
        else:
            messagebox.showwarning('Error', 'Password cannot contain special characters.')
    return new_folder_path, new_folder_value

# Close GUI:
# The below function is used for closing the main\base Tkinter window
def close_window():
    base_window.destroy()

# Close after creating new profile:
# Function will create a new profile and close the Tkinter window
def create_and_close():
    create_new_profile()
    close_window()

# Cancel GUI:
# Function closes the Tkinter GUI
def cancel_window():
    sys.exit()

# Close button:
# The below function is used for controlling the actions of X button
def clicking_x_button():
    close = messagebox.askokcancel('Close window', 'Do you really want to close?')
    if close:
        sys.exit()

# Reading faces:
# Function for animating reading faces text 
def build_data():
    loop_index = 1
    while loop_index <= 10:
        loop_index += 1
        sys.stdout.write('\r[BUILD]   Building face data \\')
        time.sleep(0.1)
        sys.stdout.write('\r[BUILD]   Building face data |')
        time.sleep(0.1)
        sys.stdout.write('\r[BUILD]   Building face data /')
        time.sleep(0.1)
        sys.stdout.write('\r[BUILD]   Building face data -')
        time.sleep(0.1)

# Training faces:
# Function for animating training faces text 
def training_model():
    loop_index = 1
    while loop_index <= 10:
        loop_index += 1
        sys.stdout.write('\r[TRAIN]   Training Face Model \\')
        time.sleep(0.1)
        sys.stdout.write('\r[TRAIN]   Training Face Model |')
        time.sleep(0.1)
        sys.stdout.write('\r[TRAIN]   Training Face Model /')
        time.sleep(0.1)
        sys.stdout.write('\r[TRAIN]   Training Face Model -')
        time.sleep(0.1)

# Text XY Position:
# Function for calculating the display text size
def text_xy_pos(text):
    text_size = cv2.getTextSize(text, font, 0.5, 2)[0]
    text_x = (gray_feed.shape[1] - text_size[0]) / 2
    text_y = (gray_feed.shape[0] + text_size[1]) / 2
    return text_x, text_y

# Face alignment:
# Function used for aligning the tilted faces
def align_face(input_feed, angle):
    if angle == 0: return input_feed
    height, width = input_feed.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 0.9)
    result = cv2.warpAffine(input_feed, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

# Aligned faces coords:
# Function for calculating compensating coords for aligned face
def align_face_coords(pos, input_feed, angle):
    if angle == 0: return pos
    x = pos[0] - input_feed.shape[1] * 0.4
    y = pos[1] - input_feed.shape[0] * 0.4
    new_x = x * cos(radians(angle)) + y * sin(radians(angle)) + input_feed.shape[1] * 0.4
    new_y = -x * sin(radians(angle)) + y * cos(radians(angle)) + input_feed.shape[0] * 0.4
    return int(new_x), int(new_y), pos[2], pos[3]

# Face detected HUD:
# Function displays the rounded rectangle around the detected face
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

# Banner frame:
config_profile_banner_frame = Frame(base_window)
config_profile_banner_frame.grid(row=0)
config_profile_banner = ImageTk.PhotoImage(Image.open(images_directory + 'Create_New_Profile_Banner.png'))
config_profile_banner_label = Label(config_profile_banner_frame, image=config_profile_banner)
config_profile_banner_label.grid(row=0)

# Configuration frame:
config_frame = LabelFrame(base_window, text='Configure Profile')
config_frame.grid(row=1, column=0, sticky='', padx=(5, 5), pady=(0, 5))

# Name:
Label(config_frame, text='Enter Name :').grid(row=0, column=0, sticky=W, padx=7, pady=5)
folder_name = StringVar()
input_folder_name = Entry(config_frame, textvariable=folder_name, width=33)
input_folder_name.grid(row=0, column=1, sticky='', padx=(1, 10), pady=(3, 0))

# Enterprise ID:
Label(config_frame, text='Enterprise ID :').grid(row=1, column=0, sticky=W, padx=7, pady=0)
enterprise_id_variable = StringVar()
enterprise_id = Entry(config_frame, textvariable=enterprise_id_variable, width=33)
enterprise_id.grid(row=1, column=1, sticky='', padx=(1, 10), pady=(0, 5))

# Environment buttons frame:
environment_buttons_frame = LabelFrame(base_window, text='Choose Environment')
environment_buttons_frame.grid(row=2, column=0, sticky='', padx=(5, 5), pady=(0, 5))

# Environment:
rdp_environment_variable = IntVar()
rmgp = Radiobutton(environment_buttons_frame, text='PROD  ', variable=rdp_environment_variable, value=1)
rmgp.grid(row=1, column=1, sticky='', padx=(1, 10), pady=(0, 5))
rmgv = Radiobutton(environment_buttons_frame, text='PREPROD', variable=rdp_environment_variable, value=2)
rmgv.grid(row=1, column=2, sticky='', padx=(1, 10), pady=(0, 5))
rmgn = Radiobutton(environment_buttons_frame, text='TEST  ', variable=rdp_environment_variable, value=3)
rmgn.grid(row=1, column=3, sticky='', padx=(1, 10), pady=(0, 5))
dev = Radiobutton(environment_buttons_frame, text='DEV   ', variable=rdp_environment_variable, value=4)
dev.grid(row=1, column=4, sticky='', padx=(1, 10), pady=(0, 5))

# Environment credentials frame:
environment_frame = LabelFrame(base_window, text='Environment Credentials')
environment_frame.grid(row=3, column=0, sticky='', padx=(5, 5), pady=(0, 5))

# User ID:
Label(environment_frame, text='User ID :      ').grid(row=0, column=0, sticky=W, padx=7, pady=0)
rdp_user_id_variable = StringVar()
rdp_user_id = Entry(environment_frame, textvariable=rdp_user_id_variable, width=33)
rdp_user_id.grid(row=0, column=1, sticky='', padx=(1, 10), pady=(0, 5))

# Password:
Label(environment_frame, text='Password :     ').grid(row=1, column=0, sticky=W, padx=7, pady=0)
rdp_password_variable = StringVar()
rdp_password = Entry(environment_frame, textvariable=rdp_password_variable, width=33, show='•')
rdp_password.grid(row=1, column=1, sticky='', padx=(1, 10), pady=(0, 5))

# Create profile button:
Label(base_window, text='All fields are mandatory', fg='red').grid(row=4, column=0, sticky=W, padx=7, pady=0)
save_button = Button(base_window, text='Create Profile', command=create_and_close, width=13).grid(row=4, column=0, sticky=E, padx=(1, 10), pady=(2, 5))

# Looping window:
base_window.protocol('WM_DELETE_WINDOW', clicking_x_button)
base_window.mainloop()

# Creating script folder:
script_folder = new_folder_path + 'Script\\'
if not os.path.exists(script_folder):
    os.makedirs(script_folder)
user_rdp_login_script = open(script_folder + new_folder_value.lower() + '_rdp_login.ps1', 'w+')
user_rdp_login_script.write('powershell.exe -ExecutionPolicy Bypass -file ' + rdp_login_script + ' "' + rdp_environment_value + '" "' + rdp_user_id_value + '" "' + rdp_password_value + '" "no" "ALL"')
user_rdp_login_script.close()

# Face Recognizer:
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Output live feed:
live_capture = cv2.VideoCapture(0)
frames_to_be_captured = 500

# Start face capture:
while (filename <= frames_to_be_captured):
    ret, color_feed = live_capture.read()
    gray_feed = cv2.cvtColor(color_feed, cv2.COLOR_BGR2GRAY)

    for angle in [0, -30, 30]:
        tilted_face = align_face(gray_feed, angle)
        face_in_feed = face_cascade.detectMultiScale(tilted_face, scaleFactor=1.3, minNeighbors=5)
        if len(face_in_feed):
            face_in_feed = [align_face_coords(face_in_feed[-1], gray_feed, -angle)]
            break

    warning_pos = text_xy_pos(warning_text)
    waiting_pos = text_xy_pos(waiting_text)
    face_cap_pos = text_xy_pos(face_capture_started)

    if len(face_in_feed) == 0:
        cv2.rectangle(color_feed, (5, 5), (int(waiting_pos[0] * 2 + 20), int(waiting_pos[1] * 0.16) + 5), red, 1)
        cv2.rectangle(color_feed, (10, 10), (int(waiting_pos[0] * 2 + 15), int(waiting_pos[1] * 0.16)), black, -1)
        cv2.putText(color_feed, waiting_text, (15, 30), font, 0.5, red, 1,  cv2.LINE_AA)
    elif len(face_in_feed) > 1:
        color_feed = cv2.GaussianBlur(color_feed, (25, 25), 3)
        cv2.rectangle(color_feed, (int(warning_pos[0]) - 15, int(warning_pos[1]) - 25), (int(warning_pos[0]) + (int(warning_pos[0] * 1.42) + 80), int(warning_pos[1]) + 15), white, 1)
        cv2.rectangle(color_feed, (int(warning_pos[0]) - 10, int(warning_pos[1]) - 20), (int(warning_pos[0]) + (int(warning_pos[0] * 1.42) + 75), int(warning_pos[1]) + 10), black, -1)
        cv2.putText(color_feed, warning_text, (int(warning_pos[0]), int(warning_pos[1])), font_duplex, 0.5, red, 1,  cv2.LINE_AA)
    elif len(face_in_feed) == 1:
        captured = '{0} of {1} FRAMES CAPTURED'.format(filename, frames_to_be_captured)
        cv2.rectangle(color_feed, (5, 5), (int(face_cap_pos[0] + 78), int(face_cap_pos[1] * 0.16) + 5), white, 1)
        cv2.rectangle(color_feed, (10, 10), (int(face_cap_pos[0]) + 73, int(face_cap_pos[1] * 0.16)), black, -1)
        cv2.putText(color_feed, captured, (15, 30), font, 0.5, white, 1,  cv2.LINE_AA)

        # Facial Landmarks:
        for (x, y, w, h) in face_in_feed:
            face_hud(color_feed, x, y, w, h, yellow)
            r = int(w / 20)
            face_detection_box_using_dlib = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
            detected_landmarks = facial_landmarks_cascade(color_feed, face_detection_box_using_dlib).parts()
            facial_landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])
            for idx, point in enumerate(facial_landmarks):
                position = (point[0, 0], point[0, 1])
                cv2.circle(color_feed, position, 0, white, -1)

            # Focusing on face:
            roi_gray_feed = gray_feed[y:y + h, x:x + w]
            roi_color_feed = color_feed[y:y + h, x:x + w]
            new_face = new_folder_path + str(filename) + '.png'
            cv2.imwrite(new_face, roi_gray_feed)
            filename += 1

    # Output window:
    cv2.imshow('Face Capture', color_feed)
    if cv2.waitKey(5) & 0xFF == int(27):
        break

# Releasing object:
live_capture.release()
cv2.destroyAllWindows()

face_id = 0
faces_array = {}
IDs = []
FaceList = []

# Texts:
print('[INFO]    Creating directory named "{}" under .\\Faces\\'.format(new_folder_value))
build_data()
print('\n[BUILD]   BUILD STATUS:', colored('SUCCESS!', 'green'))

# Saving face images:
for root, dirs, files in os.walk(faces_directory):
    for file in files:
        if file.endswith('png') or file.endswith('jpg') or file.endswith('jpeg') or file.endswith('JPG'):
            path = os.path.join(root, file)
            face_name = os.path.basename(os.path.dirname(path)).replace(' ', '-')
            if not face_name in faces_array:
                faces_array[face_name] = face_id
                face_id += 1

            ID = faces_array[face_name]

            face_image = PIL.Image.open(path).convert('L')
            face_numpy_array = np.array(face_image, 'uint8')
            face_in_folder = face_cascade.detectMultiScale(face_numpy_array, scaleFactor=1.3, minNeighbors=5)

            # Face dimensions:
            for (x, y, w, h) in face_in_folder:
                roi_face_image = face_numpy_array[y:y + h, x:x + w]
                FaceList.append(roi_face_image)
                IDs.append(ID)

# Saving pickle file:
with open(models_directory + 'Faces.pickle', 'wb') as f:
    pickle.dump(faces_array, f)

# Saving Trained model:
training_model()
face_recognizer.train(FaceList, np.array(IDs))
print('\n[TRAIN]   Training complete.\n[EXPORT]  Extracting model..\n[EXPORT]  Saving model...')
face_recognizer.save(models_directory + 'FaceModel.yml')
print(colored('[SUCCESS]', 'green'), ' Face model saved.', colored('\n[EXIT]', 'blue'), '    Terminating console.')
