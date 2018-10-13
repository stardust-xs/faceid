# FaceID
The project involves the use of Intel's OpenCV library in conjunction with Python for Face Detection, Identification and Recognition.


**Author:** XA

Requirements
---
**Versions of Python supported:**
- [Python 3.5+](https://www.python.org/downloads/)

**Python packages required:**

The project itself is purely based upon Python with some dependencies on modules or packages outside the standard Python distribution. Ensure you install the packages mentioned in the requirement.txt file or have it updated before running the code.

**External files required:**

* Haar Classifier
* Dlib 68 points shape predictor

Versions
---
**Latest stable build:**
* 1.2
  * Disabled facial landmarks from the code
  * Added support for more colours
  * Face detection box now covers the entire face instead of being a square

**Experimental build:**
* 1.1
  * Using CV2 Polylines for displaying the facial landmarks

**Known bugs**
* Application tends to get slow when multiple faces are added to it.
* Cannot distinguish between multiple users with same name.

Credits
---
* Credits for the Remote Desktop Login application go to Saktikanta for his fine powershell scripts.
* Credits for building single user detect-action logic goes to Pratijeet Bhawsar and Sachin Sanap.
