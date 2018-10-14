<h1 align="center">FaceID</h1> <br>
<p align="center">
  <a href="https://gitpoint.co/">
    <img alt="GitPoint" title="GitPoint" src="http://i.imgur.com/VShxJHs.png" width="450">
  </a>
</p>

<p align="center">
Your face is the new password. Built in Python.

</p>

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
	- [Cloning Repository](#cloning-repository)
	- [Installing Python](#installing-python)
	- [Dependencies](#dependencies)
- [How To Use?](#how-to-use)


## Introduction
The project involves the use of Intel's OpenCV library in conjunction with Python for Realtime Face Detection, Identification and Recognition. The sole purpose of this project is to eliminate the process of typing passwords for logging into Remote Desktop and running applications within it using Python's massive package repo.

## Getting Started
The code is primarily built in python with support for both MacOS and Windows, however the code will work effiicenly on Windows  due to the packages which natively supports Windows scaling.

* ### Cloning Repository

	* If you've already installed Python and OpenCV dependencies in your system you can skip the below steps and clone the repositiory in your system by pasting `git clone https://github.com/xames3/FaceID.git` in Command prompt or in Terminal.

* ### Installing Python

	* Although Python 2.7 is supported as well, it is strongly recommended to clone the project against the latest Python 3.x or minimum 3.5.x build whenever possible. That will ensure that some of the newer features of the used packages, such as speedup mechanisms of OpenCV and Pyautogui's `pyautogui.locateOnScreen` work out of the box without any issues. <br/>
	You can find all Python 3.x builds [here](https://www.python.org/downloads/).
    
    * Once you've installed Python in your system make sure you update the **pip** file using `python -m pip install --upgrade pip` command.
    
* ### Dependencies

	*  After pip is updated to update all the standard built-in packages using the `pip install --upgrade <packagename>` command or use my [pip updater](https://) file for updating it automatically.<br/>
    * For this project we need the below mentioned Python packages to be installed:
    	* OpenCV: `pip install --upgrade opencv-contrib-python`
        * Cmake: `pip install --upgrade cmake`
        * Boost: `pip install --upgrade boost`
        * Dlib: `pip install --upgrade dlib`
        * Pillow: `pip install --upgrade pillow`
        * Pyautogui: `pip install --upgrade pyautogui`
        * Openpyxl: `pip install --upgrade openpyxl`
        * xlrd: `pip install --upgrade xlrd`
    * We need [Haar Classifiers](https://) and [Dlib's Facial Landmarks](https://) to be downloaded both of which are present in project files under [Cascades](https://).
    
## How To Use?
Once you clone repo in your system all you need to do is run the **Launcher** file.Setup your face by creating a new profile and adding the terminal credentials using the `Configure` button.

## To - Do
* ### Features Planned
  - Making the Face recognition model more robust and reliable.
  - Support for password encryption in the excels files.
* ### Known bugs
  - Application tends to get slow when multiple faces are added to it.
  - Cannot distinguish between multiple users with same name.

## Version History
You can find the changelog of version [here](https://).
* ### Latest Build
	* 2.0.2
    	- Bug fixes, stability improvements.
    	- Added support for tilted face detection upto 30°.
    	- Disabled facial landmarks from the code.
		- Added support for more colours.
		- Face detection box now covers the entire face instead of being a square.
    	- Added support for .xlsx files while storing the data.
        - Minor text fixes, etc.

* ### Experimental Build
	* Beta - 2.1
    	- Using polylines for displaying Facial Landmarks instead of dots.
     
     
## Credits
* Credits for the Remote Desktop Login application go to Saktikanta for his fine powershell scripts.
* Credits for building single user detect-action logic goes to Pratijeet Bhawsar and Sachin Sanap.

## Contributions
 *  ### Contributor Guidelines 
 	* Feel free to contribute to the project by creating another branch under your name.
    
    * Make sure to use informative commit message so as to help other developers understand the done changes.
    * Stick to minimal and simplistic approach of coding using comments wherever necessary

## License
 GNU GPL v3.0
