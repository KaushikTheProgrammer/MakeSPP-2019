# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC90f079a5489b8cb3980a7c08e5d0f6ea'
auth_token = '0b7adcb970830513ce6ae468edd6c535'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Jiebin I am going to kill you.",
                     from_='+18482334348',
                     to='+17323547753'
                 )

print(message.sid)