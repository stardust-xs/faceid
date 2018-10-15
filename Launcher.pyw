# Standard package import:
import os
import sys
import ctypes
import subprocess
import win32process
from tkinter import *
from tkinter import messagebox

# From packages import:
from PIL import Image, ImageTk

# Directory declaration:
root_directory = os.path.dirname(os.path.abspath(__file__))
binaries_directory = os.path.join(root_directory, 'Binaries\\')
faces_directory = os.path.join(root_directory, 'Faces\\')
if not os.path.exists(faces_directory):
    os.makedirs(faces_directory)
images_directory = os.path.join(root_directory, 'Images\\')

# GUI base window object
base_window = Tk()

# GUI window:
# The below function is a Tkinter window which will act as the base window for the setup. The window is centered in the screen.
def window(main):
	main.title('XA FaceID')
	main.resizable(0, 0)
	main.update_idletasks()
	width = 324
	height = 150
	win_x_pos = (main.winfo_screenwidth() // 2) - (width // 2)
	win_y_pos = (main.winfo_screenheight() // 2) - (height // 2)
	main.geometry('{}x{}+{}+{}'.format(width, height, win_x_pos, win_y_pos))
	main.iconbitmap(images_directory + 'xa_logo.ico')
window(base_window)

# Cancel button:
# Cancels\Exits the UI
def cancel_window():
	sys.exit()

# Close button:
# The below function is used for controlling the actions of X button
def clicking_x_button():
	close = messagebox.askokcancel('Close window', 'Do you really want to close?')
	if close:
		sys.exit()

# Close GUI:
# The below function is used for closing the main\base Tkinter window
def close_after_launching_face_id():
	base_window.destroy()

# FaceID:
# Opens FaceID script
def face_id():
    os.startfile('FaceID.py')

# Bypass FaceID:
# Closes current window and opens FaceID
def launch_face_id_and_close():
	close_after_launching_face_id()
	face_id()

# Admin login window:
# Displays Admin login prompt
def admin_login():
    os.startfile('Admin.pyw')

# Banner Frame:
config_profile_banner_frame = Frame(base_window)
config_profile_banner_frame.grid(row = 0)
config_profile_banner = ImageTk.PhotoImage(Image.open(images_directory + 'Face_ID_Banner.png'))
config_profile_banner_label = Label(config_profile_banner_frame, image = config_profile_banner)
config_profile_banner_label.grid(row = 0)

# Configuration Frame:
config_frame = LabelFrame(base_window, text = 'Face ID')
config_frame.grid(row = 1, column = 0, sticky = '', padx = (5, 5), pady = (0, 5))

# Adding Buttons:
stop_button = Button(config_frame, text = 'Configure', command = admin_login, width = 11).grid(row = 1, column = 1, sticky = '', padx = 7, pady = 10)
face_id_button = Button(config_frame, text = 'Run Face ID', command = launch_face_id_and_close, width = 11).grid(row = 1, column = 2, sticky = '', padx = 10, pady = 10)
cancel_button = Button(config_frame, text = 'Cancel', command = cancel_window, width = 11).grid(row = 1, column = 3, sticky = '', padx = 7, pady = 10)

# Looping Window:
base_window.protocol('WM_DELETE_WINDOW', clicking_x_button)
base_window.mainloop()