import io
import os
import cv2
import time
import threading 
import runtime

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('MakeSPP.json')

# Instantiates a client
client = vision.ImageAnnotatorClient(credentials=credentials)

file_name = 'images/live.jpg'

isQuit = False

def analyzeFrame():

    while not isQuit:
        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        for label in labels:
            print(label.description)

if __name__ == "__main__":

    t1 = threading.Thread(target=analyzeFrame) 
    t1.start() 

    frame_counter = 0
    cap = cv2.VideoCapture('images/robbery.mp4')

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_counter += 1
        
        cv2.imshow('frame', frame)

        if frame_counter > 29:
            cv2.imwrite(file_name, frame)
            frame_counter = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            isQuit = True
            break
        
    t1.join()     

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print("done")
