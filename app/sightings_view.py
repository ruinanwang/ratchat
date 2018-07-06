
import requests
from . import app, db, geocoder
from . import config, prompts
from flask import request, session, redirect, url_for
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

@app.route('/sighting', methods=['GET'])
def sighting():
    response = MessagingResponse()
    message = Message()
    user_input = request.values.get('Body', None)
    user_input_test = user_input.replace(' ', '').replace('\n', '')
    counter = session.get('counter', 0)
    mistakes = session.get('mistakes', 0)
    
    if counter == 1:
        message.body(prompts.sighting_address)
        session['counter'] = counter + 1
    elif counter == 2:
        lat, lon, address = geocoder.geocode(user_input.replace('\n', ' '))
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif lat != None and lon != None and address != None:
            db.query(config.db_credentials, config.update_sighting_address_sql, (address, lat, lon, session['row_id']))
            message.body(prompts.in_out)
            session['counter'] = counter + 1
            session['mistakes'] = 0
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.sighting_address_error)

    elif counter == 3:
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif user_input_test == '1':
            db.query(config.db_credentials, config.update_sighting_in_out_sql, (0, session['row_id']))
            message.body(prompts.dead_or_alive)
            session['counter'] = counter + 1
            session['mistakes'] = 0
        elif user_input_test == '2':
            db.query(config.db_credentials, config.update_sighting_in_out_sql, (1, session['row_id']))
            message.body(prompts.dead_or_alive)
            session['counter'] = counter + 1
            session['mistakes'] = 0
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.in_out_error)
        
    elif counter == 4:
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif user_input_test == '1':
            db.query(config.db_credentials, config.update_sighting_dead_alive_sql, (0, session['row_id']))
            message.body(prompts.sighting_picture)
            session['counter'] = counter + 1
            session['mistakes'] = 0
        elif user_input_test == '2':
            db.query(config.db_credentials, config.update_sighting_dead_alive_sql, (1, session['row_id']))
            message.body(prompts.sighting_picture)
            session['counter'] = counter + 1
            session['mistakes'] = 0
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.dead_or_alive_error)
        
    elif counter == 5:
        if user_input_test.upper() == 'RESTART':
            response.redirect(url=url_for('restart'), method='GET')
            return str(response)
        elif request.values['NumMedia'] != '0':
            filename = request.values['MessageSid'] + '.jpg'
            filepath = config.sighting_image_directory + filename
            with open(filepath, 'wb') as f:
                image_url = request.values['MediaUrl0']
                f.write(requests.get(image_url).content)
            db.query(config.db_credentials, config.update_sighting_image_sql, (filepath, session['row_id']))
            db.query(config.db_credentials, config.update_sighting_finished_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.report_complete)
        elif user_input_test.upper() == 'DONE':
            db.query(config.db_credentials, config.update_sighting_finished_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.report_complete)   
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if mistakes == 3:
                response.redirect(url=url_for('mistakes'), method='GET')
                return str(response)
            message.body(prompts.sighting_picture_error)           

    response.append(message)
    return str(response)