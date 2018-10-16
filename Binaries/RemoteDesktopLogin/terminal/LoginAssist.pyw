# Standard package import:
import os
import time

# From packages import:
import pyautogui
import keyboard

# Directories declaration:
root_directory = os.path.dirname(os.path.abspath('__file__'))
screenshots_directory = os.path.join(root_directory, 'screenshots\\')

# Image variables:
ok_image = screenshots_directory + 'ok.PNG'
hta_gui_image = screenshots_directory + 'hta_gui.PNG'
start_image = screenshots_directory + 'start.PNG'
ie_yellow_image = screenshots_directory + 'ie_yellow.PNG'
maximize_image = screenshots_directory + 'maximize.PNG'

def click_on_visible(image, padding_x=0, padding_y=0, secs=0):
	image_button = None
	while image_button is None:
		image_button = pyautogui.locateOnScreen(image)
	image_button =  pyautogui.locateOnScreen(image)
	image_button_x, image_button_y = pyautogui.center(image_button)
	pyautogui.click(image_button_x + padding_x, image_button_y + padding_y)
	time.sleep(secs)

def doubleclick_on_visible(image, padding_x=0, padding_y=0, secs=0):
	image_button = None
	while image_button is None:
		image_button = pyautogui.locateOnScreen(image)
	image_button =  pyautogui.locateOnScreen(image)
	image_button_x, image_button_y = pyautogui.center(image_button)
	pyautogui.doubleClick(image_button_x + padding_x, image_button_y + padding_y)
	time.sleep(secs)

def wait_till_visible(image):
	image_button = None
	while image_button is None:
		image_button = pyautogui.locateOnScreen(image)

pyautogui.FAILSAFE = False
pyautogui.doubleClick(0, 0, _pause=False)
keyboard.write('OneClick_v4')
keyboard.press('enter')
wait_till_visible(hta_gui_image)
keyboard.write('Click to open GUI.hta')
keyboard.press('enter')
click_on_visible(start_image)
click_on_visible(ie_yellow_image)
click_on_visible(maximize_image, padding_y=-32)