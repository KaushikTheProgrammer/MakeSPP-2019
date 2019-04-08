from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from sightengine.client import SightengineClient
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
import threading
import smtplib

file_name = "image.jpg"
framespeed = 1/60
client = SightengineClient('1968420216', 'SdWBjWBcGSQWtW9Qkiiq')
frame_counter = 0
cap = cv2.VideoCapture('images/storerobbery.mp4')
weaponFlag = False

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
detected = False


# Definition of Kivy App instance
class DisplayWindow(App):
    global weaponFlag
    # Defining window contents
    def build(self):
        # Layout of window to contain image and label attributes
        self.layout = BoxLayout(orientation="vertical")
        self.title_text = Label(text="DeTECT-ProTECT", size_hint=(1, .1))
        self.image = Image(source=file_name, size_hint=(1, .7))
        self.output = Label(text="one", size_hint=(1, .1))
        # Dynamic callbacks scheduled with Clock to display video feed and analysis
        Clock.schedule_interval(self.labelCallback, framespeed)
        Clock.schedule_interval(self.videoCallback, framespeed)
        # Adding attributes to box as widgets
        self.layout.add_widget(self.title_text)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.output)
        return self.layout

    # Reloads image from the disk with specified refresh rate
    def videoCallback(self, dt):
        # Capture frame-by-frame
        global cap
        ret, frame = cap.read()
        global frame_counter
        frame_counter += 1

        cv2.imwrite(file_name, frame)
        self.image.reload()
    
    # Refreshes label at specified time interval, checking for change in detection boolean
    def labelCallback(self, dt):
        if weaponFlag:
            self.output.text = "Weapon detected! Call the proper authorities!"
        else:
            self.output.text = ""


def analyzeFrame():
    while True:
        global frame_counter
        global weaponFlag
        global detected
        if not detected:
            output = client.check('wad').set_file(file_name)
            if output['status'] != 'failure':
                if output['weapon'] > 0.1:
                    if not detected:
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
                        weaponFlag = True
                        detected = True
                        print(message.sid)
            frame_counter = 0


if __name__ == "__main__":

    t2 = threading.Thread(target=analyzeFrame)
    t2.start()

    DisplayWindow().run()

    t2.join()

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print("done")
