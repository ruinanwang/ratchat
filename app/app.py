
import config
import prompts
import requests
from db_handler import DB
from geocoder import Geocoder
from flask import Flask, request, session, render_template, url_for
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

db = DB()
app = Flask(__name__)
app.secret_key = config.secret_key
app.config.from_object(__name__)
geocoder = Geocoder(config.api_key)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.route('/sms', methods=['POST'])
def sms():
    response = MessagingResponse()
    message = Message()
    counter = session.get('counter', 0)

    if not counter:
        if request.values['NumMedia'] != '0':
            filename = request.values['MessageSid'] + '.jpg'
            filepath = config.image_directory + filename
            with open(filepath, 'wb') as f:
                image_url = request.values['MediaUrl0']
                f.write(requests.get(image_url).content)
            db.query(config.db_credentials, config.insert_report)
            session['row_id'] = db.getRowId()

            db.query(config.db_credentials, config.update_image, (filepath, session['row_id']))
            session['counter'] = 1
            message.body(prompts.address_image)
        else:
            db.query(config.db_credentials, config.insert_report)
            session['row_id'] = db.getRowId()
            session['counter'] = 1
            message.body(prompts.address)
        response.append(message)
        return str(response)
    else:
        if counter == 1:
            response.redirect(url=url_for('address'), method='POST')
            return str(response)
        elif counter == 2:
            response.redirect(url=url_for('options'), method='POST')
            return str(response)

@app.route('/sms/address', methods=['POST'])
def address():
    response = MessagingResponse()
    message = Message()
    user_input = request.values.get('Body', None).replace('\n', ' ')
    mistakes = session.get('mistakes', 0)

    lat, lon, address = geocoder.geocode(user_input)
    if lat != None and lon != None and address != None:
        db.query(config.db_credentials, config.update_address, (address, lat, lon, session['row_id']))
        session['counter'] = 2
        session['mistakes'] = 0
        message.body(prompts.options)
    else:
        session['mistakes'] = mistakes + 1
        if session['mistakes'] == 3:
            response.redirect(url=url_for('mistakes'), method='GET')
            return str(response)
        message.body(prompts.address_error)  

    response.append(message)
    return str(response)

@app.route('/sms/options', methods=['POST'])
def options():
    response = MessagingResponse()
    message = Message()
    user_input = request.values.get('Body', None).replace(' ', '').replace('\n', '').upper()
    mistakes = session.get('mistakes', 0) 

    if user_input == 'A':
        db.query(config.db_credentials, config.update_sighting, ('sighting', 'outside', 'alive', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'B':
        db.query(config.db_credentials, config.update_sighting, ('sighting', 'inside', 'alive', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'C':
        db.query(config.db_credentials, config.update_sighting, ('sighting', 'outside', 'dead', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'D':
        db.query(config.db_credentials, config.update_sighting, ('sighting', 'inside', 'dead', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'E':
        db.query(config.db_credentials, config.update_evidence, ('evidence', 'chewed', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'F':
        db.query(config.db_credentials, config.update_evidence, ('evidence', 'droppings', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'G':
        db.query(config.db_credentials, config.update_evidence, ('evidence', 'hole', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    else:
        session['mistakes'] = mistakes + 1
        if session['mistakes'] == 3:
            response.redirect(url=url_for('mistakes'), method='GET')
            return str(response)
        message.body(prompts.option_error)        

    response.append(message)
    return str(response)

@app.route('/sms/mistakes', methods=['GET'])
def mistakes():
    response = MessagingResponse()
    message = Message()
    counter = session.get('counter', 0)
    user_input = request.values.get('Body', None)

    if counter == 1:
        db.query(config.db_credentials, config.update_mistakes_address, (user_input, 0, 0, 1, session['row_id']))
    elif counter == 2:
        db.query(config.db_credentials, config.update_mistakes_options, (user_input, 1, session['row_id']))
        
    session.clear()
    message.body(prompts.mistakes)
    response.append(message)
    return str(response)