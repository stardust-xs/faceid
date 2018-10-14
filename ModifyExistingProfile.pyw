# Standard import:
import os
import sys
import time
import shutil
import base64
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

# Excel objects:
resource_details = load_workbook(excels_directory + 'ResourceDetails.xlsx')
resource_data = resource_details['Resource_Data']

# RDP object:
rdp_login_script = (binaries_directory + 'RemoteDesktopLogin\\config\\rdp_auto_login.ps1')

# Tkinter window object:
search_window = Tk()

# Variables:
last_empty_row = resource_data.max_row + 1

# GUI window:
# The below function is a Tkinter window which will act as the base window for the setup. The window is centered in the screen.
def window(main):
    main.title('XA FaceID')
    main.resizable(0, 0)
    main.update_idletasks()
    width = 325
    height = 303
    win_x = (main.winfo_screenwidth() // 2) - (width // 2)
    win_y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, win_x, win_y))
    main.iconbitmap(images_directory + 'xa_logo.ico')
window(search_window)

# Search name:
# The below function is used for searching the name in ResourceDetails excel file
def search_name():
    global search_resource
    global matched_row
    global current_password_value
    search_resource = input_folder_name.get()
    if len(input_folder_name.get()) == 0:
        messagebox.showwarning('Error', 'Please enter a name.')
        sys.exit()
    elif len(input_folder_name.get()) > 16:
        messagebox.showwarning('Error', 'Maximum 15 characters are allowed.')
    elif len(input_folder_name.get()) <= 15:
        allowed_characters = set('0123456789_abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ/')
        if set(input_folder_name.get()).issubset(allowed_characters):
            for search_row in resource_data.rows:
                if search_row[0].value == search_resource:
                    messagebox.showinfo('Success', '1 Match found - {0}'.format(search_row[0].value))
                    input_folder_name.config(state=DISABLED)
                    current_password.config(state=NORMAL, textvariable='')
                    new_password.config(state=NORMAL)
                    re_enter_password.config(state=NORMAL)
                    matched_row = search_row[0].row
                    current_password_value = resource_data['XA{}'.format(matched_row)].value
                    return search_resource, current_password_value, matched_row
        else:
            messagebox.showwarning('Error', 'Name cannot contain special characters.')

def search_and_close():
    search_name()

def update_profile():
    global login_flag
    global search_row
    if len(current_password.get()) == 0:
        messagebox.showwarning('Error', 'Please enter the current password.')
    elif len(current_password.get()) > 21:
        messagebox.showwarning('Error', 'Password cannot contain more than 20 characters.')
    elif len(current_password.get()) <= 20:
        allowed_characters = set('0123456789_abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ\\.!@#$%^&*()-;<>?|/')
        if set(current_password.get()).issubset(allowed_characters):
            if current_password_value == current_password.get():
                if len(new_password.get()) == 0:
                    messagebox.showwarning('Error', 'Please enter new password.')
                elif len(new_password.get()) > 21:
                    messagebox.showwarning('Error', 'Password cannot contain more than 20 characters.')
                elif len(new_password.get()) <= 20:
                    allowed_characters = set('0123456789_abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ\\.!@#$%^&*()-;<>?|/')
                    if set(new_password.get()).issubset(allowed_characters):
                        new_password_value = new_password.get()
                        if new_password_value == re_enter_password.get():
                            rdp_password_cell = resource_data['XA' + str(matched_row)]
                            rdp_password_cell.value = new_password.get()
                            resource_details.save(excels_directory + '\\ResourceDetails.xlsx')
                            current_password.config(state=DISABLED)
                            new_password.config(state=DISABLED)
                            re_enter_password.config(state=DISABLED)
                            messagebox.showinfo('Success', 'Password updated.')
                        else:
                            messagebox.showwarning('Error', 'Passwords don\'t match.')
                    else:
                        messagebox.showwarning('Error', 'Password cannot contain special characters.')
                else:
                    messagebox.showwarning('Error', 'Connect with the administrator.')
            else:
                messagebox.showwarning('Error', 'Current password doesn\'t match the records.')

# Close button:
# The below function is used for controlling the actions of X button
def clicking_x_button():
    close = messagebox.askokcancel('Close window', 'Do you really want to close?')
    if close:
        sys.exit()

# Banner frame:
search_profile_banner_frame = Frame(search_window)
search_profile_banner_frame.grid(row=0)
search_profile_banner = ImageTk.PhotoImage(Image.open(images_directory + 'Modify_Profile_Banner.png'))
search_profile_banner_label = Label(search_profile_banner_frame, image=search_profile_banner)
search_profile_banner_label.grid(row=0)

# Search frame:
search_frame = LabelFrame(search_window, text='Search')
search_frame.grid(row=1, column=0, sticky='', padx=(5, 5), pady=(0, 5))

# Name:
Label(search_frame, text='Enter Name :').grid(row=0, column=0, sticky=W, padx=7, pady=5)
folder_name = StringVar()
input_folder_name = Entry(search_frame, textvariable=folder_name, width=33)
input_folder_name.grid(row=0, column=1, sticky='', padx=(1, 10), pady=(3, 0))

# Search button:
search_button = Button(search_frame, text='Search Profile', command=search_and_close, width=13).grid(row=1, column=1, sticky=E, padx=(1, 10), pady=(0, 5))

# Change password frame:
modify_frame = LabelFrame(search_window, text='Change Password')
modify_frame.grid(row=2, column=0, sticky='', padx=(5, 5), pady=(0, 5))

# Current password:
Label(modify_frame, text='Current Password :').grid(row=0, column=0, sticky=W, padx=7, pady=5)
current_password_variable = StringVar()
current_password = Entry(modify_frame, textvariable=current_password_variable, width=28, show='•', state=DISABLED)
current_password.grid(row=0, column=1, sticky='', padx=(1, 10), pady=(3, 0))

# New password:
Label(modify_frame, text='New Password :').grid(row=1, column=0, sticky=W, padx=7, pady=0)
new_password_variable = StringVar()
new_password = Entry(modify_frame, textvariable=new_password_variable, width=28, show='•', state=DISABLED)
new_password.grid(row=1, column=1, sticky='', padx=(1, 10), pady=(0, 5))

# Re enter password:
Label(modify_frame, text='Re enter Password :').grid(row=2, column=0, sticky=W, padx=7, pady=0)
new_password_variable = StringVar()
re_enter_password = Entry(modify_frame, textvariable=new_password_variable, width=28, show='•', state=DISABLED)
re_enter_password.grid(row=2, column=1, sticky='', padx=(1, 10), pady=(0, 5))

# Search button:
update_button = Button(search_window, text='Update Profile', command=update_profile, width=13).grid(row=3, column=0, sticky=E, padx=(1, 10), pady=(0, 5))

# Looping window:
search_window.protocol('WM_DELETE_WINDOW', clicking_x_button)
search_window.mainloop()