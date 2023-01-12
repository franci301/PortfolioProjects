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

client = Client(account_sid,auth_token)


# https://www.twilio.com/blog/whatsapp-recipe-bot-python-flask-mongodb-twilio


@app.route('/whatsapp', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if '@help' in incoming_msg:
        quote = 'List of commands:\n\n@birthday followed by the persons *name* and *DOB* you wish to see their birthday for.\n\n@lazysearch followed by the persons *first name* or *last name* to view every person with that firstname/lastname\n\n@add followed by the persons *name* and *birthday* to add their birthday to the system. \n\n@age followed by the persons *name* to view their current age\n\n@edit followed by the *name* and *birthday* of the user to edit followed by a *"/"* followed by the *name* and *birthday* of the corrected version\n\n@delete followed by the *name* and *birthday* of the user to delete\n\n@viewAll to view all users in the database\n\n@examples to see examples of how to use these commands'
        msg.body(quote)
        responded = True
    if '@examples' in incoming_msg:
        quote = 'List of examples\n\n@birthday Francesco Gregotti 08 January 2002\n\n@lazysearch Francesco\n\n@add Francesco Gregotti 08 January 2002\n\n@edit Francesco Gregotti 08 January 2002 / Francesco Gregotti 20 January 2001\n\n@age Francesco Gregotti\n\n@delete Francesco Gregotti 08 January 2002\n\n@viewAll'
        msg.body(quote)
        responded = True
    if '@birthday' in incoming_msg:
        name = incoming_msg.split(' ',1)[1]
        birthday = logic.search_birthday(name)
        message = convertToMessage.convert_result_to_message(birthday)
        msg.body(message)
        responded = True
    if '@add' in incoming_msg:
        data = incoming_msg.split(' ',1)[1]
        logic.add(data)
        msg.body('Added to the database')
        responded = True
    if '@age' in incoming_msg:
        data = incoming_msg.split(' ',1)[1]
        birthday = logic.search_birthday(data)
        stringData = json_to_string.convert(birthday)
        age = calc.calculate_age(stringData)
        string = f'{stringData[0]} is {age} years old'
        msg.body(string)
        responded = True
    if '@lazysearch' in incoming_msg:
        res = logic.lazy_search(incoming_msg.split(' ',)[1])
        final = convertToMessage.convert_result_to_message(res)
        msg.body(final)
        responded = True
    if '@viewAll' in incoming_msg:
        # displays all the users in the database
        allData = logic.search_all()
        message = convertToMessage.convert_result_to_message(allData)
        msg.body(message)
        responded = True
    if '@edit' in incoming_msg:
        # edit the details of a user in the database
        data = incoming_msg.split(' ',1)[1]
        stringData = convertDouble.convertBoth(data)
        logic.edit(stringData)
        msg.body('Edited successfully')
        responded = True
    if '@delete' in incoming_msg:
        # delete a user in the database
        data = incoming_msg.split(' ',1)[1]
        logic.deleteOne(data)
        msg.body('Deleted successfully')
        responded = True
    if not responded:
        msg.body('Sorry i dont know that command - If you need help type: @help')
    return str(resp)

# ERROR THROWN DISPLAY MESSAGE AND RESTART SERVICE
# EVERY DAY CHECK IF A BIRTHDAY IS EQUAL TO TODAY --> IF IT IS THEN SEND THE NOTIFICATION REMINDER WITH A PRE LOADED MESSAGE
# ADD AN OPTION TO CUSTOMISE A PRELOADED MESSAGE WHICH WILL BE SENT TO THE GROUPCHAT ON A PERSONS BIRTHDAY

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)