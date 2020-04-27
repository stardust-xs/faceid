
<h1 align="center">
  FaceID
  <br>
</h1>

<h4 align="center">Your face is the new password. Built in <a href="https://www.python.org/downloads/" target="_blank">Python</a>.</h4>

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#code">Code</a> •
  <a href="#pipeline">Pipeline</a> •
  <a href="#version-history">Version History</a> •
  <a href="#contribution">Contribution</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

<h1 align="center">
  <br>
  <img alt="FaceIDLogin" title="FaceIDLogin" src="https://github.com/xames3/FaceID/blob/repository_assets/FaceIDLogin.gif?raw=true" width="1000"></a>
  <br>

## Introduction
The project involves the use of Intel's OpenCV library in conjunction with Python for realtime Face Detection and Recognition. The sole purpose of this project is to eliminate the process of typing passwords for logging into Remote Desktop and running applications within it using Python's massive package repo.

## Getting Started
The code is primarily built in python with support for both Mac OS and Windows, however the code will work efficiently on Windows due to the packages which natively supports Windows scaling.
* [Cloning Repository](#cloning-repository)
* [Installing Python](#installing-python)
* [Dependencies](#dependencies)
* [Choosing IDE](#choosing-ide)
	 * ### Cloning Repository
	      * If you've Python and OpenCV dependencies already installed in your system you can skip the below steps and clone the repository in your system by pasting `git clone https://github.com/xames3/FaceID.git` in CMD or Terminal. I'm using [GitBash](https://git-scm.com/downloads) here.
	  <p align="center"> 
	      <img alt="GitClone" title="GitClone" src="https://github.com/xames3/FaceID/blob/repository_assets/GitClone.gif?raw=true" width="507"><p/>
	 * ### Installing Python
	      * Although Python 2.7 is supported as well, it is strongly recommended to clone the project against the latest Python 3.x or minimum 3.5.x builds whenever possible. This will ensure that some of the newer features of the used packages, such as speedup mechanisms of OpenCV and Pyautogui's `pyautogui.locateOnScreen` work out of the box without any issues. You can find all Python 2 and 3 builds [here](https://www.python.org/downloads/).
	     * Once you've installed Python in your system make sure you update **pip** using `python -m pip install --upgrade pip` command in CMD or Terminal.

	 * ### Dependencies
	     * After pip is updated, update all the standard built-in packages using the `pip install --upgrade <packagename>` command or use my [pip updater](https://github.com/xames3/FaceID/blob/repository_assets/pip_updater.py) code for updating it automatically. Please be patient as it may take sometime depending upon speed of your internet.

	     * For FaceID to be working we need the below mentioned Python packages to be installed:
		      * OpenCV: `pip install --upgrade opencv-contrib-python`
		      * Cmake: `pip install --upgrade cmake`
		      * Boost: `pip install --upgrade boost`
		      * Dlib: `pip install --upgrade dlib`
		      * Pillow: `pip install --upgrade pillow`
		      * Pyautogui: `pip install --upgrade pyautogui`
		      * Openpyxl: `pip install --upgrade openpyxl`
		      * xlrd: `pip install --upgrade xlrd`
		      * Colorama: `pip install --upgrade colorama`
	 
	 
	     * We need [Haar Classifiers](https://github.com/opencv/opencv/tree/master/data/haarcascades) and [Dlib's Facial Landmarks](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) to be downloaded both of which are present in project files under [Cascades](https://github.com/xames3/FaceID/tree/master/Cascades).

	 * ### Choosing IDE
	      * You can use any Python supporting IDE of your preference. I prefer working on [Sublime Text 3](https://www.sublimetext.com/3) due to it's Package Control system and useful plugins for Python.
    
## Code
The logic built around the program is to first detect face(s) in the visible feed. If the face(s) are detected the program will try to recognize the face\person using the dynamically trained model. The code is built in 3 primary stages.
* [Face Detection](#face-detection)
* [Face Recognition](#face-recognition)
* [RDP Login](#rdp-login)
	 * ### Face Detection
		 ```python
		 while (True):
		 ret, color_feed = live_capture.read()
		 gray_feed = cv2.cvtColor(color_feed, cv2.COLOR_BGR2GRAY)
		 face_in_feed = face_cascade.detectMultiScale(gray_feed, scaleFactor=1.3, minNeighbors=5)
		 if len(face_in_feed) == 0:
		 ...
		 elif len(face_in_feed) > 3:
		 ...
		 else:
		 ...
		 ```
		* The above snippet checks if there are any faces in the output window `color_feed`. If face(s) are found it takes respective actions using the ```if-elif-else``` condititons.

     * ### Face Recognition

		 ```python
		 face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		 ...
		 labels = {}
		 face_recognizer.read(models_directory + 'FaceModel.yml')
		 with open(models_directory + 'Faces.pickle', 'rb') as f:
		     og_labels = pickle.load(f)
		     labels = {v: k for k, v in og_labels.items()}
		 ...
		 ID, confidence = face_recognizer.predict(roi_gray_feed)
		 identified = 'Matched : {}%'.format(str(round(confidence)))
		 ```
		* The above snippet is fundamental piece of code for identifying the face\person in the output window.

     * ### RDP Login

		 ```python
		 ...
		 os.startfile(faces_directory + labels[ID] + '\\Script\\' + labels[ID].lower() + '_rdp_login.ps1')
		 os.startfile(binaries_directory + 'OnscreenChecker\\LoginAssist.py')
		 ...
		 ```
		* These 2 lines work upon the Remote Desktop Login and further automation using [PyAutoGUI](https://pypi.org/project/PyAutoGUI/), a Python native GUI automation package. The `labels[ID].lower() + '_rdp_login.ps1'` is Sakti's RDP login script modified for that specific user.

		* **For example:** If you create a new Face profile with name **John** then this file will be autogenerated as `'john_rdp_login.ps1'` with your RDP login credentials.<br/>
	    Thanks to Sakti's help his file dynamics can start bruteforcing his App and log the user into RDP.
	    Once the user is logged into RDP, PyAutoGUI takes over the control using `pyautogui.locateOnScreen` command for navigating through the GUI.
     	
## Pipeline

Pipeline shows the scope of the project
* [Planned Features](#planned-features)
* [Known Issues](#known-issues)
	 * ### Planned Features
	    * Converting into an executable file.
	    * Making the Face recognition model more robust and reliable.
	    * Support for password encryption in the excels files.
	    
	 * ### Known Issues
	    * Application tends to get slow when multiple faces are detected.
	    * Cannot distinguish between multiple users with same name. (Fixed)
	    * Code does not support ML yet.
	    * FaceID fails under low-lighting conditions.
  
## Version History
You can find the changelog of version [here](https://).
* [Latest Build](#latest-build)
* [Experimental Build](#experimental-build)
	 * ### Latest Build
		* Stable: 2.1
		* Bug fixes, stability improvements.
		* Added support for tilted face detection upto 30°.
		* Facial landmarks are now slightly accurate.
		* Added support for more colours.
		* Face detection box now covers the entire face instead of being a square.
		* Added support for .xlsx files while storing the data.
		* Minor text fixes, etc.

	 * ### Experimental Build
		* RC: 2.1.0
		* Using polylines for displaying Facial Landmarks instead of dots. 
	
## Contribution
Feel free to send pull requests and raise issues.
* Feel free to contribute to the project by mirroring another branch with distinct name so as to avoid confusions.
* Stick to minimal and simplistic approach of coding using comments wherever necessary.
    
## Credits
* [Sakti](https://github.com/saktikanta) for his Powershell based Remote Desktop login app.
* Pratijeet Bhawsar and Sachin Sanap for helping develop single user detection action logic.

## License
FaceID is an open source project licensed under GNU GPL v3.0.
