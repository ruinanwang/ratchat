
import config
import prompts
import requests
from db_handler import DB
from geocoder import Geocoder
from datetime import timedelta
from flask import Flask, request, session, render_template, url_for
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

db = DB()
app = Flask(__name__)
app.secret_key = config.secret_key
app.config.from_object(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
geocoder = Geocoder(config.api_key)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', data=[2,3])

@app.route('/sms', methods=['POST'])
def sms():
    session.permanent = True
    response = MessagingResponse()
    message = Message()
    counter = session.get('counter', 0)
    num_images = eval(request.values['NumMedia'])

    if not counter:
        if num_images != 0:
            if  num_images > 1:
                message.body(prompts.too_many_images)
                response.append(message)
                return str(response)
            filename = request.values['MessageSid'] + '.jpg'
            filepath = config.image_directory + filename
            with open(filepath, 'wb') as f:
                image_url = request.values['MediaUrl0']
                f.write(requests.get(image_url).content)
            db.execute(config.db_credentials, config.insert_report_original)
            db.execute(config.db_credentials, config.insert_report_altered)
            session['row_id'] = db.get_row_id()
            db.execute(config.db_credentials, config.update_image_original, (filepath, session['row_id']))
            db.execute(config.db_credentials, config.update_image_altered, (filepath, session['row_id']))
            session['counter'] = 1
            message.body(prompts.address_image)
        else:
            db.execute(config.db_credentials, config.insert_report_original)
            db.execute(config.db_credentials, config.insert_report_altered)
            session['row_id'] = db.get_row_id()
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
    user_input_test = user_input.replace(' ', '')
    lat, lon, address = geocoder.geocode(user_input)

    if user_input_test.upper() == 'YES' and 'address' in session:
        db.execute(config.db_credentials, config.update_address_original, (session['address'], None, None, session['row_id']))
        db.execute(config.db_credentials, config.update_address_altered, (session['address'], None, None, session['row_id']))
        session['counter'] = 2
        message.body(prompts.options)
    elif user_input_test.isnumeric() or user_input_test.isalpha():
        message.body(prompts.partial_address)
    elif lat != None and lon != None and address != None:
        db.execute(config.db_credentials, config.update_address_original, (address, lat, lon, session['row_id']))
        db.execute(config.db_credentials, config.update_address_altered, (address, lat, lon, session['row_id']))
        session['counter'] = 2
        message.body(prompts.options)
    else:
        session['address'] = user_input
        message.body(prompts.address_error)  

    response.append(message)
    return str(response)

@app.route('/sms/options', methods=['POST'])
def options():
    response = MessagingResponse()
    message = Message()
    user_input = request.values.get('Body', None).replace(' ', '').replace('\n', '').upper()

    if user_input == 'A':
        db.execute(config.db_credentials, config.update_sighting_original, ('sighting', 'outside', 'alive', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_sighting_altered, ('sighting', 'outside', 'alive', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'B':
        db.execute(config.db_credentials, config.update_sighting_original, ('sighting', 'inside', 'alive', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_sighting_altered, ('sighting', 'inside', 'alive', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'C':
        db.execute(config.db_credentials, config.update_sighting_original, ('sighting', 'outside', 'dead', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_sighting_altered, ('sighting', 'outside', 'dead', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'D':
        db.execute(config.db_credentials, config.update_sighting_original, ('sighting', 'inside', 'dead', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_sighting_altered, ('sighting', 'inside', 'dead', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'E':
        db.execute(config.db_credentials, config.update_evidence_original, ('evidence', 'chewed', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_evidence_altered, ('evidence', 'chewed', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'F':
        db.execute(config.db_credentials, config.update_evidence_original, ('evidence', 'droppings', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_evidence_altered, ('evidence', 'droppings', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    elif user_input == 'G':
        db.execute(config.db_credentials, config.update_evidence_original, ('evidence', 'hole', 1, session['row_id']))
        db.execute(config.db_credentials, config.update_evidence_altered, ('evidence', 'hole', 1, session['row_id']))
        session.clear()
        message.body(prompts.done)
    else:
        db.execute(config.db_credentials, config.update_evidence_original, (user_input, None, 0, session['row_id']))
        db.execute(config.db_credentials, config.update_evidence_altered, (user_input, None, 0, session['row_id']))
        message.body(prompts.option_error)        

    response.append(message)
    return str(response)