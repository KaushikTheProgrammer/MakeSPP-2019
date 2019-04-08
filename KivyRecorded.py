from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from sightengine.client import SightengineClient
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
from threading import Thread
import smtplib
import copy
import numpy as np
from PIL import Image as PILImage
import time

file_name = "image.jpg"
fps = 60
client = SightengineClient('1968420216', 'SdWBjWBcGSQWtW9Qkiiq')
cap = cv2.VideoCapture('images/storerobbery.mp4')
ret, frame = cap.read()
newFrame = PILImage.fromarray(frame)
detected = False
request_complete = True

# create message object instance
msg = MIMEMultipart()
 
 
message = "Gun Detected! ACT IMMEDIATELY!"
 
# setup the parameters of the message
password = "MakeSPP-2019"
msg['From'] = "makesppdetector@gmail.com"
msg['To'] = "kaushikpprakash@gmail.com"
msg['Subject'] = "Gun Detected! ACT IMMEDIATELY!"
 
# add in the message body
msg.attach(MIMEText(message, 'plain'))
 
#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)

account_sid = 'AC90f079a5489b8cb3980a7c08e5d0f6ea'
auth_token = '0b7adcb970830513ce6ae468edd6c535'
twilioClient = Client(account_sid, auth_token)


def analyzeFrame():
    global detected
    global request_complete
    global newFrame
    request_complete = False
    newFrame.save(file_name)
    print("file saved")
    if not detected:
        start = time.process_time()
        output = client.check('wad').set_file(file_name)
        end = time.process_time()
        print("output received in %s seconds" % (end - start))
        print(output)
        if output['status'] != 'failure':
            if output['weapon'] > 0.1:
                print("detected")
                message = twilioClient.messages \
                    .create(
                    body="Gun Detected! ACT IMMEDIATELY!",
                    from_='+18482334348',
                    to='+17327725794'
                )
                message = twilioClient.messages \
                    .create(
                    body="Gun Detected! ACT IMMEDIATELY!",
                    from_='+18482334348',
                    to='+18482188011'
                )
                # send the message via the server.
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.sendmail(msg['From'], "mwolak07@gmail.com", msg.as_string())
                server.quit()
                print("successfully sent email to %s:" % (msg['To']))
                detected = True
                print(message.sid)
    request_complete = True


process = Thread(target=analyzeFrame)
process.start()

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        global request_complete
        global process
        global newFrame
        ret, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if request_complete:
            process.join()
            newFrame = PILImage.fromarray(frame)
            process = Thread(target=analyzeFrame)
            process.start()
        if ret:
        # convert it to texture
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


# Definition of Kivy App instance
class DisplayWindow(App):
    global weaponFlag
    # Defining window contents
    def build(self):
        # Layout of window to contain image and label attributes
        self.layout = BoxLayout(orientation="vertical")
        self.title_text = Label(text="DeTECT-ProTECT", size_hint=(1, .1))
        self.camera = KivyCamera(capture=cap, fps=fps)
        self.output = Label(text="one", size_hint=(1, .1))
        # Dynamic callbacks scheduled with Clock to display video feed and analysis
        Clock.schedule_interval(self.labelCallback, 1.0/fps)
        # Adding attributes to box as widgets
        self.layout.add_widget(self.title_text)
        self.layout.add_widget(self.camera)
        self.layout.add_widget(self.output)
        return self.layout
    
    # Refreshes label at specified time interval, checking for change in detection boolean
    def labelCallback(self, dt):
        if detected:
            self.output.text = "Weapon detected! Call the proper authorities!"
        else:
            self.output.text = ""

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        cap.release()

DisplayWindow().run()
process.join()
