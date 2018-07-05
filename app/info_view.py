
from . import app
from . import prompts
from flask import Flask, session
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

@app.route('/info', methods=['GET'])
def info():
    response = MessagingResponse()
    message = Message()

    session.clear()
    message.body(prompts.prevention_prompt)
    response.append(message)
    return str(response)




