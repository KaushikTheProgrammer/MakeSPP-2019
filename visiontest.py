import io
import os
import cv2
import time

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('MakeSPP.json')

# Instantiates a client
client = vision.ImageAnnotatorClient(credentials=credentials)

cap = cv2.VideoCapture(0)

# The name of the image file to annotate
file_name = 'images/live.jpg'

frame_counter = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_counter += 1

    if frame_counter > 29:
        cv2.imwrite(file_name, frame)

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        for label in labels:
            print(label.description, label.score)

        frame_counter = 0

    cv2.imshow('currFrame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()