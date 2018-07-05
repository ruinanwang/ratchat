
from . import app, db
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

@app.route('/sms', methods=['POST'])
def sms():
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
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        if user_input_test == '1':
            session['case'] = 1
            session['mistakes'] = 0
            db.query(config.add_sighting_sql)
            session['row_id'] = db.getRowId()
            response.redirect(url=url_for('sighting'), method='GET')
            return str(response)
        elif user_input_test == '2':
            session['case'] = 2
            session['mistakes'] = 0
            db.query(config.add_evidence_sql)
            session['row_id'] = db.getRowId()
            response.redirect(url=url_for('evidence'), method='GET')
            return str(response)
        elif user_input_test == '3':
            session['case'] = 3
            session['mistakes'] = 0
            response.redirect(url=url_for('info'), method='GET')
            return str(response)
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.welcome_error)
            response.append(message)
            return str(response)
    else:
        if case == 1:
            response.redirect(url=url_for('sighting'), method='GET')
            return str(response)
        elif case == 2:
            response.redirect(url=url_for('evidence'), method='GET')
            return str(response)
        elif case == 3:
            response.redirect(url=url_for('info'), method='GET')
            return str(response)
