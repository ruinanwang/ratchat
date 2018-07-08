
from db_handler import DB
from sms import prompts
import config
from flask import session
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

db = DB()

def mistakes():
    response = MessagingResponse()
    message = Message()
    counter = session.get('counter', 0)
    case = session.get('case', 0)

    if case == 1:
        if counter == 2:
            db.query(config.db_credentials, config.update_sighting_address_sql, (None, 0, 0, session['row_id']))
            db.query(config.update_sighting_mistake_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.mistakes_prompt)
            response.append(message)
            return str(response)
        else:
            db.query(config.db_credentials, config.update_sighting_mistake_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.mistakes_prompt)
            response.append(message)
            return str(response)
    elif case == 2:
        if counter == 2:
            db.query(config.db_credentials, config.update_evidence_address_sql, (None, 0, 0, session['row_id']))
            db.query(config.db_credentials, config.update_evidence_mistake_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.mistakes_prompt)
            response.append(message)
            return str(response)
        else:
            db.query(config.db_credentials, config.update_evidence_mistake_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.mistakes_prompt)
            response.append(message)
            return str(response)
    else:
        session.clear()
        message.body(prompts.mistakes_prompt)
        response.append(message)
        return str(response)
