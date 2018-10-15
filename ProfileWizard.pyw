# Standard import:
import os
import sys
import time
import win32process
from tkinter import *
from tkinter import StringVar
from tkinter import messagebox

# Downloaded packages import:
import cv2
import dlib
import pickle
import openpyxl as xl
import PIL.Image
import numpy as np
from openpyxl import *
from PIL import Image, ImageTk

# Directories declaration:
root_directory = os.path.dirname(os.path.abspath(__file__))
binaries_directory = os.path.join(root_directory, 'Binaries\\')
excels_directory = os.path.join(root_directory, 'Excels\\')
faces_directory = os.path.join(root_directory, 'Faces\\')
if not os.path.exists(faces_directory):
    os.makedirs(faces_directory)
images_directory = os.path.join(root_directory, 'Images\\')

# Tkinter window object:
base_window = Tk()

# GUI window:
# The below function is a Tkinter window which will act as the base window for the setup. The window is centered in the screen.
def window(main):
    main.title('XA FaceID')
    main.resizable(0, 0)
    main.update_idletasks()
    width = 326
    height = 150
    win_x = (main.winfo_screenwidth() // 2) - (width // 2)
    win_y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, win_x, win_y))
    main.iconbitmap(images_directory + 'xa_logo.ico')
window(base_window)

# Close GUI:
# The below function is used for closing the main\base Tkinter window
def close_window():
    base_window.destroy()

# Close after creating new profile:
# Function will create a new profile and close the Tkinter window
def create_and_close():
    create_new_profile()
    close_window()

def create_new_profile():
    os.startfile('SetupFacialRecognition.py')

def modify_profile():
    os.startfile('ModifyExistingProfile.pyw')

# Close after modifying new profile:
# Function will modify existing profile and close the Tkinter window
def modify_and_close():
    modify_profile()
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

# Cancel button:
# Cancels\Exits the UI
def cancel_window():
	sys.exit()

# Banner frame:
config_profile_banner_frame = Frame(base_window)
config_profile_banner_frame.grid(row=0)
config_profile_banner = ImageTk.PhotoImage(Image.open(images_directory + 'Profile_Wizard_Banner.png'))
config_profile_banner_label = Label(config_profile_banner_frame, image=config_profile_banner)
config_profile_banner_label.grid(row=0)

# Configuration frame:
config_frame = LabelFrame(base_window, text='Profile Wizard')
config_frame.grid(row=1, column=0, sticky='', padx=(5, 5), pady=(0, 5))

# Create profile button:
save_button = Button(config_frame, text='Create New', command=create_and_close, width=12).grid(row=1, column=1, sticky='', padx = 4, pady = 10)
modify_button = Button(config_frame, text='Modify Existing', command=modify_and_close, width=12).grid(row=1, column=2, sticky='', padx = (2, 4), pady = 10)
cancel_button = Button(config_frame, text = 'Cancel', command = cancel_window, width = 12).grid(row = 1, column = 3, sticky = '', padx = (2, 4), pady = 10)

# Looping window:
base_window.protocol('WM_DELETE_WINDOW', clicking_x_button)
base_window.mainloop()