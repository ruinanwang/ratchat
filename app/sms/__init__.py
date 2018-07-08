
import config
from sms import prompts 
from db_handler import DB
from sms.sightings_view import sighting
from sms.evidence_view import evidence
from sms.info_view import info
from sms.restart_view import restart
from sms.mistakes_view import mistakes
from flask import Blueprint, request, session, redirect, url_for
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

db = DB()
sms = Blueprint('sms', __name__, url_prefix='/sms')
sms.add_url_rule('/sighting', None, sighting, methods=['POST'])
sms.add_url_rule('/evidence', None, evidence, methods=['POST'])
sms.add_url_rule('/info', None, info, methods=['GET'])
sms.add_url_rule('/restart', None, restart, methods=['GET'])
sms.add_url_rule('/mistakes', None, mistakes, methods=['GET'])

@sms.route('/', methods=['POST'])
def process_message():
    response = MessagingResponse()
    message = Message()
    user_input = str(request.values.get('Body', None))
    user_input_test = user_input.replace(' ', '').replace('\n', '')
    counter = session.get('counter', 0)
    case = session.get('case', 0)
    mistakes = session.get('mistakes', 0)

    # Start of report.
    if not counter:
        message.body(prompts.welcome)
        session['counter'] = 1
        response.append(message)
        return str(response)
    elif not case: 
        if user_input_test.upper() == 'RESTART':
            response.redirect(url_for('sms.restart'))
            return str(response)
        if user_input_test == '1':
            session['case'] = 1
            session['mistakes'] = 0
            db.query(config.db_credentials, config.add_sighting_sql)
            session['row_id'] = db.getRowId()
            response.redirect(url_for('sms.sighting'))
            return str(response)
        elif user_input_test == '2':
            session['case'] = 2
            session['mistakes'] = 0
            db.query(config.db_credentials, config.add_evidence_sql)
            session['row_id'] = db.getRowId()
            response.redirect(url_for('sms.evidence'))
            return str(response)
        elif user_input_test == '3':
            session['case'] = 3
            session['mistakes'] = 0
            response.redirect(url_for('sms.info'))
            return str(response)
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url_for('sms.mistakes'))
                return str(response)
            message.body(prompts.welcome_error)
            response.append(message)
            return str(response)
    else:
        if case == 1:
            response.redirect(url_for('sms.sighting'))
            return str(response)
        elif case == 2:
            response.redirect(url_for('sms.evidence'))
            return str(response)
        elif case == 3:
            response.redirect(url_for('sms.info'))
            return str(response)

