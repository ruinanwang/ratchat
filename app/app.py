
import config
import prompts
import requests
import mysql.connector
from db_handler import DB
from geocoder import Geocoder
from mysql.connector import errorcode
from flask import Flask, request, session, render_template, url_for
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

app = Flask(__name__)
app.secret_key = config.secret_key
app.config.from_object(__name__)
db = DB()
geocoder = Geocoder(config.api_key)

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
            db.query(config.db_credentials, config.add_sighting_sql)
            session['row_id'] = db.getRowId()
            response.redirect(url=url_for('sighting'), method='POST')
            return str(response)
        elif user_input_test == '2':
            session['case'] = 2
            session['mistakes'] = 0
            db.query(config.db_credentials, config.add_evidence_sql)
            session['row_id'] = db.getRowId()
            response.redirect(url=url_for('evidence'), method='POST')
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
            response.redirect(url=url_for('sighting'), method='POST')
            return str(response)
        elif case == 2:
            response.redirect(url=url_for('evidence'), method='POST')
            return str(response)
        elif case == 3:
            response.redirect(url=url_for('info'), method='GET')
            return str(response)

@app.route('/sms/sighting', methods=['POST'])
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

@app.route('/sms/evidence', methods=['POST'])
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
            db.query(config.db_credentials, config.update_evidence_address_sql, (address, lat, lon, session['row_id']))
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
            db.query(config.db_credentials, config.update_evidence_category_sql, (1, 0, session['row_id']))
            session['counter'] = counter + 1
            session['mistakes'] = 0
            message.body(prompts.evidence_picture)
        elif user_input_test == '2':
            db.query(config.db_credentials, config.update_evidence_category_sql, (0, 1, session['row_id']))
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
            db.query(config.db_credentials, config.update_evidence_image_sql, (filepath, session['row_id']))
            db.query(config.db_credentials, config.update_evidence_finished_sql, (1, session['row_id']))
            session.clear()
            message.body(prompts.report_complete)
        elif user_input_test.upper() == 'DONE':
            db.query(config.db_credentials, config.update_evidence_finished_sql, (1, session['row_id']))
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

@app.route('/sms/info', methods=['GET'])
def info():
    response = MessagingResponse()
    message = Message()

    session.clear()
    message.body(prompts.prevention_prompt)
    response.append(message)
    return str(response)

@app.route('/sms/restart', methods=['GET'])
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

@app.route('/sms/mistakes', methods=['GET'])
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