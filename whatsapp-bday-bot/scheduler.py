from flask import Flask, request
import requests
import convertToMessage
import calc
import json_to_string
import re
import upcoming
import logic
import os
import convertDouble
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.twiml.messaging_response import MessagingResponse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler


db = firestore.client()
collection = db.collection('check')
app = Flask(__name__)
account_sid = 'ACefa837a93bd287d3b281f55fbb0b523e'
auth_token = 'b29b7298d29a1c1575c6ef6671d6e667'
client = Client(account_sid,auth_token)


resp = MessagingResponse()
msg = resp.message()
upcomingBirthdays = upcoming.checkUpcoming()
if(len(upcomingBirthdays) != 0):
    for i in range(len(upcomingBirthdays)):
        message = client.messages.create(
            body=f"It is {upcomingBirthdays[i][0]}'s birthday today! Remember to wish them a happy birthday",
            from_='whatsapp:+14155238886',
            to='whatsapp:+447711143105'
        )
else:
    message = client.messages.create(
        body="There are no birthdays today",
        from_='whatsapp:+14155238886',
        to='whatsapp:+447711143105'
    )

# sched = BackgroundScheduler()
# sched.add_job(check_dates, 'cron', hour=13, minute=24)
# sched.start()