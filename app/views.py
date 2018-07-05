
from . import app
from . import report_view
from . import sightings_view
from . import evidence_view
from . import info_view
from . import restart_view
from . import mistakes_view
from . import config, prompts
from flask import Flask, request, session, redirect, url_for, render_template
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', data=[1,2,3,4])

