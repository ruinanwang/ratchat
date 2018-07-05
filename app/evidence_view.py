
import requests
from . import app, db, geocoder
from . import config, prompts
from flask import Flask, request, session, redirect, url_for
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

@app.route('/evidence', methods=['GET'])
def evidence():
    response = MessagingResponse()
    message = Message()
    user_input = request.values.get('Body', None)
    user_input_test = user_input.replace(' ', '').replace('\n', '')
    counter = session.get('counter', 0)
    mistakes = session.get('mistakes', 0) 

    if counter == 1:
        message.body(prompts.evidence_address)
        session['counter'] = counter + 1
    elif counter == 2:
        lat, lon, address = geocoder.geocode(user_input.replace('\n', ' '))
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif lat != None and lon != None and address != None:
            db.query(config.update_evidence_address_sql, (address, lat, lon, session['row_id']))
            message.body(prompts.category)
            session['counter'] = counter + 1
            session['mistakes'] = 0
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.evidence_address_error)

    elif counter == 3:
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif user_input_test == '1':
            db.query(config.update_evidence_category_sql, (1, 0, session['row_id']))
            session['counter'] = counter + 1
            session['mistakes'] = 0
            message.body(prompts.evidence_picture)
        elif user_input_test == '2':
            db.query(config.update_evidence_category_sql, (0, 1, session['row_id']))
            session['counter'] = counter + 1
            session['mistakes'] = 0
            message.body(prompts.evidence_picture)
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.category_error)
        
    elif counter == 4:
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif request.values['NumMedia'] != '0':
            filename = request.values['MessageSid'] + '.jpg'
            filepath = config.evidence_image_directory + filename
            with open(filepath, 'wb') as f:
                image_url = request.values['MediaUrl0']
                f.write(requests.get(image_url).content)
            db.query(config.update_evidence_image_sql, (filepath, session['row_id']))
            db.query(config.update_evidence_finished_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.report_complete)
        elif user_input_test.upper() == 'DONE':
            db.query(config.update_evidence_finished_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.report_complete)   
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.evidence_picture_error)            

    response.append(message)
    return str(response)