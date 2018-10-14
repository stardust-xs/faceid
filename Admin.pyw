# Standard package import:
import os
import sys
import base64
from tkinter import *
from tkinter import messagebox

# From packages import:
from openpyxl import *
from pyautogui import press
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
encrypted_data = resource_details['Encrypted'] # Sheet name

# Tkinter window object:
login_window = Tk()

# GUI window:
# The below function is a Tkinter window which will act as the base window for the setup. The window is centered in the screen.
def window(main):
    main.title('XA FaceID')
    main.resizable(0, 0)
    main.update_idletasks()
    width = 324
    height = 204
    win_x_pos = (main.winfo_screenwidth() // 2) - (width // 2)
    win_y_pos = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, win_x_pos, win_y_pos))
    main.iconbitmap(images_directory + 'xa_logo.ico')
window(login_window)

# Login button:
# The below function is used for logging into the FaceID UI
def login():
    global login_flag
    encrypted_admin_key = encrypted_data['XA68'].value
    encrypted_user_name = base64.b64encode(bytes(u'' + login_user_name.get(), 'utf-8'))
    decrypted_user_name = base64.b64decode(encrypted_user_name).decode('utf-8', 'ignore')
    string_encrypted_user_name = str(encrypted_user_name)

    encrypted_admin_password = encrypted_data['XA69'].value
    encrypted_password = base64.b64encode(bytes(u'' + login_password.get(), 'utf-8'))
    decrypted_password = base64.b64decode(encrypted_password).decode('utf-8', 'ignore')
    string_encrypted_password = str(encrypted_password)

    if encrypted_admin_key == string_encrypted_user_name:
        if encrypted_admin_password == string_encrypted_password:
            login_flag = 1
            login_window.destroy()
        else:
            messagebox.showwarning('Warning', 'Error while Login. Please check the entered password!')
            sys.exit()
    else:
        messagebox.showerror('Error', 'Invalid Credentials!')
        sys.exit()

# Show password check box:
# This function is show password checkbox
def show_password():
    if show_password_variable.get() == 1:
        input_password = Entry(login_frame, textvariable=login_password, width=35)
        input_password.grid(row=2, column=1, sticky='', padx=(0, 10), pady=(0, 0))
    else:
        input_password = Entry(login_frame, textvariable=login_password, width=35, show='•')
        input_password.grid(row=2, column=1, sticky='', padx=(0, 10), pady=(0, 0))

# Close button
# The below function is used for controlling the actions of X button
def clicking_x_button():
    close = messagebox.askokcancel('Close window', 'Do you really want to cancel?')
    if close:
        sys.exit()

# Close GUI
# The below function is used for closing the main\base Tkinter window
def close_after_launching_face_id():
    base_window.destroy()

# Bypass Login
# Function will login into the UI and then launch Setup file
def login_successful():
    login()
    os.system('ProfileWizard.pyw')

# Banner frame:
admin_banner_frame = Frame(login_window)
admin_banner_frame.grid(row=0)
admin_banner = ImageTk.PhotoImage(Image.open(images_directory + 'Admin_Banner.png'))
admin_banner_label = Label(admin_banner_frame, image=admin_banner)
admin_banner_label.grid(row=0)

# Login frame:
login_frame = LabelFrame(login_window, text='Admin Login')
login_frame.grid(row=1, column=0, sticky='', padx=(5, 5), pady=0)

# Username label:
Label(login_frame, text='Username :').grid(row=1, column=0, sticky=W, padx=7, pady=5)
login_user_name = StringVar()
input_user_name = Entry(login_frame, textvariable=login_user_name, width=35)
input_user_name.grid(row=1, column=1, sticky='', padx=(0, 10), pady=5)

# Password label:
Label(login_frame, text='Password :').grid(row=2, column=0, sticky=W, padx=7, pady=0)
login_password = StringVar()
input_password = Entry(login_frame, textvariable=login_password, width=35, show='•')
input_password.grid(row=2, column=1, sticky='', padx=(0, 10), pady=0)

# Show password check box:
show_password_variable = BooleanVar()
show_password_checkbox = Checkbutton(login_frame, text='Show', command=show_password, variable=show_password_variable)
show_password_checkbox.grid(row=3, column=0, sticky=W, padx=7, pady=10)

# Login button:
login_button = Button(login_frame, text='Login', command=login_successful, width=10)
login_button.grid(row=3, column=1, sticky=E, padx=(0, 10), pady=10)

# Looping window:
login_window.protocol('WM_DELETE_WINDOW', clicking_x_button)
login_window.mainloop()