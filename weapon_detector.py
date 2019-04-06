# if you haven't already, install the SDK with "pip install sightengine"
from sightengine.client import SightengineClient
import cv2

cap = cv2.VideoCapture('images/storerobbery.mp4')

frame_counter = 0
file_name = 'images/live.jpg'
client = SightengineClient('185769829', 'b8CCfNrKrYnWYwsUeBbK')

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_counter += 1
    
    cv2.imshow('frame', frame)

    if frame_counter == 10:
        cv2.imwrite(file_name, frame)
        output = client.check('wad').set_file('images/live.jpg')
        print(output)
        frame_counter = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        isQuit = True
        break        

