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
- opencv                --> (pip3 install opencv-python)
- sightengine           --> (pip3 install sightengine)
- kivy                  --> (pip3 install kivy)
- twilio                --> (pip3 install twilio)
- PIL                   --> (pip3 install pillow)

Team:
Mateusz Wolak, Kaushik Prakash