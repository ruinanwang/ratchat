
from sms import prompts
from flask import session
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

def info():
    response = MessagingResponse()
    message = Message()

    session.clear()
    message.body(prompts.prevention_prompt)
    response.append(message)
    return str(response)




