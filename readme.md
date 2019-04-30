2019 MakeSPP hackathon project

Description
- Detects weapon from video stream (live or pre-recorded) and
	  sends text message and email when weapon is found, with gui 
	  for display
- OpenCV used for acces to camera and mp4 file reading
- Kivy used to build gui
- smtp lib used for email
- twilio used for text messages
- sightengine used for weapon detection
- threading used to run video stream & gui on seperate thread from analysis

Environment:
- python version: 3.6
- opencv                --> (pip install opencv-python)
- sightengine           --> (pip install sightengine)
- kivy                  --> (pip install kivy)
- twilio                --> (pip install twilio)
- PIL                   --> (pip install pillow)

*pip might default to python 2, in that case, use pip3

Team:
Mateusz Wolak, Kaushik Prakash
