
# ratwatch.py
# Flask app that interfaces with the Twilio API to create
# a SMS report for people to report rat sightings or evidence
# in the city of Atlanta. The app also stores user responses
# into a MySQL database for analysis.

import config
import prompts
import requests
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, session, render_template
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

# Establishes a connection with database.
db_credentials = config.db_credentials
try:
    connection = mysql.connector.connect(**db_credentials)
    cursor = connection.cursor()
except mysql.connector.Error:
    raise

# Configures and starts the application.
SIGHTING_IMAGE_DOWNLOAD_DIRECTORY = config.sighting_image_directory
EVIDENCE_IMAGE_DOWNLOAD_DIRECTORY = config.evidence_image_directory
SECRET_KEY = config.secret_key
API_KEY = config.api_key
app = Flask(__name__)
app.config.from_object(__name__)

# Prompts for the report.

# General prompts.
welcome = prompts.welcome
welcome_error = prompts.welcome_error
report_complete = prompts.report_complete
mistakes_prompt = prompts.mistakes_prompt
prevention_prompt = prompts.prevention_prompt

# Rat sighting prompts.
sighting_address = prompts.sighting_address
sighting_address_error = prompts.sighting_address_error
in_out = prompts.in_out
in_out_error = prompts.in_out_error
dead_or_alive = prompts.dead_or_alive
dead_or_alive_error = prompts.dead_or_alive_error
sighting_picture = prompts.sighting_picture
sighting_picture_error = prompts.sighting_picture_error

# Rat evidence prompts.
evidence_address = prompts.evidence_address
evidence_address_error = prompts.evidence_address_error
category = prompts.category
category_error = prompts.category_error
evidence_picture = prompts.evidence_picture
evidence_picture_error = prompts.evidence_picture_error

# SQL statements for inserting, deleting, and updating information.
add_sighting_sql = config.add_sighting_sql
add_evidence_sql = config.add_evidence_sql

update_sighting_address_sql = config.update_sighting_address_sql
update_sighting_in_out_sql = config.update_sighting_in_out_sql
update_sighting_dead_alive_sql = config.update_sighting_dead_alive_sql
update_sighting_image_sql = config.update_sighting_image_sql
update_sighting_finished_sql = config.update_sighting_finished_sql
update_sighting_restart_sql = config.update_sighting_restart_sql
update_sighting_mistake_sql = config.update_sighting_mistake_sql

update_evidence_address_sql = config.update_evidence_address_sql
update_evidence_category_sql = config.update_evidence_category_sql
update_evidence_image_sql = config.update_evidence_image_sql
update_evidence_finished_sql = config.update_evidence_finished_sql
update_evidence_restart_sql = config.update_evidence_restart_sql
update_evidence_mistake_sql = config.update_evidence_mistake_sql

# Function that geocodes an address using
# the Google Maps API.
def geocode(address):
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    parameters = {
        'key': API_KEY,
        'address': address
    }

    request = requests.get(GOOGLE_MAPS_API_URL, params=parameters)
    response = request.json()
    result = response['results']

    if (result):
        lat = result[0]['geometry']['location']['lat']
        lon = result[0]['geometry']['location']['lng']
        address = result[0]['formatted_address']
        city = ''
        for item in result[0]['address_components']:
            if item['long_name'] == 'Atlanta':
                city = item['long_name']
                return lat, lon, address, city            
        return None, None, None, None
    else:
        return None, None, None, None

# Function that returns the HTML
# info page for RatWatch.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Function that provides instructions
# to Twilio on how to respond to an
# incoming SMS message.
@app.route('/sms', methods=['GET', 'POST'])
def process_message():

    response = MessagingResponse()
    message = Message()
    user_input = request.values.get('Body', None)
    user_input_test = user_input.replace(' ', '').replace('\n', '')
    counter = session.get('counter', 0)
    case = session.get('case', 0)
    mistakes = session.get('mistakes', 0)

    # Start of report.
    if (counter == 0):
        message.body(welcome)
        session['counter'] = counter + 1
        response.append(message)
        return str(response)

    # Sets the current case based on the user's input.
    # If the user has already selected a case, then
    # the application continues.
    if (not case):
        if (user_input_test.upper() == 'RESTART'):
            message.body(welcome)
            response.append(message)
            return str(response)
        if (user_input_test == '1'):
            session['case'] = 1
            case = session.get('case', 0)
            session['mistakes'] = 0
            mistakes = session.get('mistakes', 0)
            cursor.execute(add_sighting_sql)
            session['row_id'] = cursor.lastrowid
            connection.commit()
        elif (user_input_test == '2'):
            session['case'] = 2
            case = session.get('case', 0)
            session['mistakes'] = 0
            mistakes = session.get('mistakes', 0)
            cursor.execute(add_evidence_sql)
            session['row_id'] = cursor.lastrowid
            connection.commit()
        elif (user_input_test == '3'):
            session['case'] = 3
            case = session.get('case', 0)
        else:
            session['mistakes'] = mistakes + 1
            mistakes = session['mistakes']
            if (mistakes == 3):
                session.clear()
                message.body(mistakes_prompt)
                response.append(message)
                return str(response)
            message.body(welcome_error)

    # Decision tree that carries out the appropriate 
    # logic based on the case and the counter.
    if (case == 1):

        if (counter == 1):
            message.body(sighting_address)
            session['counter'] = counter + 1
    
        elif (counter == 2):
            lat, lon, address, city = geocode(user_input.replace('\n', ' '))
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_sighting_restart_sql, (1, session['row_id'],))
                connection.commit()
                session.clear()
                session['counter'] = 1
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (lat != None and lon != None and address != None and city != None):
                if (city == 'Atlanta'):
                    cursor.execute(update_sighting_address_sql, (address, lat, lon, session['row_id']))
                    connection.commit()
                    message.body(in_out)
                    session['counter'] = counter + 1
                    session['mistakes'] = 0
                else:
                    message.body(sighting_address_error)
                    response.append(message)
                    return str(response)
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_sighting_address_sql, (user_input, 0, 0, session['row_id']))
                    cursor.execute(update_sighting_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(sighting_address_error)

        elif (counter == 3):
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_sighting_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                session['counter'] = 1       
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (user_input_test == '1'):
                cursor.execute(update_sighting_in_out_sql, (0, session['row_id']))
                connection.commit()
                message.body(dead_or_alive)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            elif (user_input_test == '2'):
                cursor.execute(update_sighting_in_out_sql, (1, session['row_id']))
                connection.commit()
                message.body(dead_or_alive)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_sighting_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(in_out_error)
            
        elif (counter == 4):
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_sighting_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                session['counter'] = 1
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (user_input_test == '1'):
                cursor.execute(update_sighting_dead_alive_sql, (0, session['row_id']))
                cursor.execute(update_sighting_finished_sql, (1, session['row_id']))
                connection.commit()
                message.body(sighting_picture)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            elif (user_input_test == '2'):
                cursor.execute(update_sighting_dead_alive_sql, (1, session['row_id']))
                cursor.execute(update_sighting_finished_sql, (1, session['row_id']))
                connection.commit()
                message.body(sighting_picture)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_sighting_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(dead_or_alive_error)
            
        elif (counter == 5):
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_sighting_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                session['counter'] = 1
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (request.values['NumMedia'] != '0'):
                filename = request.values['MessageSid'] + '.jpg'
                filepath = SIGHTING_IMAGE_DOWNLOAD_DIRECTORY + filename
                with open(filepath, 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
                cursor.execute(update_sighting_image_sql, (filepath, session['row_id']))
                connection.commit()
                session.clear()
                message.body(report_complete)
            elif (user_input_test.upper() == 'DONE'):
                session.clear()
                message.body(report_complete)   
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_sighting_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(sighting_picture_error)           

    elif (case == 2):

        if (counter == 1):
            message.body(evidence_address)
            session['counter'] = counter + 1

        elif (counter == 2):
            lat, lon, address, city = geocode(user_input.replace('\n', ' '))
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                session['counter'] = 1
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (lat != None and lon != None and address != None and city != None):
                if (city == 'Atlanta'):
                    cursor.execute(update_evidence_address_sql, (address, lat, lon, session['row_id']))
                    connection.commit()
                    message.body(category)
                    session['counter'] = counter + 1
                    session['mistakes'] = 0
                else:
                    message.body(evidence_address_error)
                    response.append(message)
                    return str(response)
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_evidence_address_sql, (user_input, 0, 0, session['row_id']))
                    cursor.execute(update_evidence_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(evidence_address_error)

        elif (counter == 3):
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                session['counter'] = 1
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (user_input_test == '1'):
                cursor.execute(update_evidence_category_sql, (1, 0, session['row_id']))
                cursor.execute(update_evidence_finished_sql, (1, session['row_id']))
                connection.commit()
                session['counter'] = counter + 1
                session['mistakes'] = 0
                message.body(evidence_picture)
            elif (user_input_test == '2'):
                cursor.execute(update_evidence_category_sql, (0, 1, session['row_id']))
                cursor.execute(update_evidence_finished_sql, (1, session['row_id']))
                connection.commit()
                session['counter'] = counter + 1
                session['mistakes'] = 0
                message.body(evidence_picture)
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_evidence_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(category_error)
            
        elif (counter == 4):
            if (user_input_test.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                session['counter'] = 1
                message.body(welcome)
                response.append(message)
                return str(response)
            elif (request.values['NumMedia'] != '0'):
                filename = request.values['MessageSid'] + '.jpg'
                filepath = EVIDENCE_IMAGE_DOWNLOAD_DIRECTORY + filename
                with open(filepath, 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
                cursor.execute(update_evidence_image_sql, (filepath, session['row_id']))
                connection.commit()
                session.clear()
                message.body(report_complete)
            elif (user_input_test.upper() == 'DONE'):
                session.clear()
                message.body(report_complete)   
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(update_evidence_mistake_sql, (1, session['row_id']))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(evidence_picture_error)            

    elif (case == 3):
        message.body(prevention_prompt)
        session.clear()

    response.append(message)
    return str(response)

if __name__ == '__main__':
    app.run()
