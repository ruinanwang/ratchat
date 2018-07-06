
from . import app, db, config, prompts
from flask import session
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

@app.route('/restart', methods=['GET'])
def restart():
    response = MessagingResponse()
    message = Message()
    counter = session.get('counter', 0)
    case = session.get('case', 0)

    if case == 1:
        db.query(config.db_credentials, config.update_sighting_restart_sql, (1, session['row_id']))
        session.clear()
        session['counter'] = 1
        message.body(prompts.welcome)
        response.append(message)
        return str(response)
    elif case == 2:
        db.query(config.db_credentials, config.update_evidence_restart_sql, (1, session['row_id']))
        session.clear()
        session['counter'] = 1
        message.body(prompts.welcome)
        response.append(message)
        return str(response)
    else:
        message.body(prompts.welcome)
        response.append(message)
        return str(response)