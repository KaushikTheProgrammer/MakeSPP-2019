"""Detects unsafe features in the file."""
from google.cloud import vision
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
import io
import os

credentials = service_account.Credentials.from_service_account_file('MakeSPP.json')

# Instantiates a client
client = vision.ImageAnnotatorClient(credentials=credentials)

with io.open("images/image3.jpg", 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.safe_search_detection(image=image)
safe = response.safe_search_annotation

# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
print('Safe search:')

print('adult: {}'.format(likelihood_name[safe.adult]))
print('medical: {}'.format(likelihood_name[safe.medical]))
print('spoofed: {}'.format(likelihood_name[safe.spoof]))
print('violence: {}'.format(likelihood_name[safe.violence]))
print('racy: {}'.format(likelihood_name[safe.racy]))