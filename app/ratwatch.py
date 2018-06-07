
# ratwatch.py
# Flask app that interfaces with the Twilio API to create
# a SMS survey for people to report rat sitings or evidence
# in the city of Atlanta. The app also stores user responses
# into a MySQL database for analysis.

import config
import prompts
import requests
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, session
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

# Establishes a connection with database.
try:
    connection = mysql.connector.connect(**config.db)
    cursor = connection.cursor()
except mysql.connector.Error:
    raise

# Configures and starts the application.
IMAGE_DOWNLOAD_DIRECTORY = config.image_directory
SECRET_KEY = config.secret_key
app = Flask(__name__)
app.config.from_object(__name__)

# Prompts for the survey.

# General prompts.
welcome = prompts.welcome
welcome_error = prompts.welcome_error
city = prompts.city
city_error = prompts.city_error
zipcode = prompts.zipcode
zipcode_error = prompts.zipcode_error
survey_complete = prompts.survey_complete
mistakes_prompt = prompts.mistakes_prompt
restart_prompt = prompts.restart_prompt

# Rat siting prompts.
site_address = prompts.site_address
site_address_error = prompts.site_address_error
in_out = prompts.in_out
in_out_error = prompts.in_out_error
dead_or_alive = prompts.dead_or_alive
dead_or_alive_error = prompts.dead_or_alive_error
site_picture = prompts.site_picture
site_picture_error = prompts.site_picture_error

# Rat evidence prompts.
evidence_address = prompts.evidence_address
evidence_address_error = prompts.evidence_address_error
category = prompts.category
category_error = prompts.category_error
evidence_picture = prompts.evidence_picture
evidence_picture_error = prompts.evidence_picture_error

# SQL statements for inserting, deleting, and updating information.
add_site_sql = config.add_site_sql
add_evidence_sql = config.add_evidence_sql

update_site_city_sql = config.update_site_city_sql
update_site_zip_sql = config.update_site_zip_sql
update_site_in_out_sql = config.update_site_in_out_sql
update_site_dead_alive_sql = config.update_site_dead_alive_sql
update_site_image_sql = config.update_site_image_sql
update_site_restart_sql = config.update_site_restart_sql

update_evidence_city_sql = config.update_evidence_city_sql
update_evidence_zip_sql = config.update_evidence_zip_sql
update_evidence_category_sql =config.update_evidence_category_sql
update_evidence_image_sql = config.update_evidence_image_sql
update_evidence_restart_sql = config.update_evidence_restart_sql

delete_site_sql = config.delete_site_sql
delete_evidence_sql = config.delete_evidence_sql

# Function that provides instructions
# to Twilio on how to respond to an
# incoming SMS message.
@app.route('/sms', methods=['GET', 'POST'])
def process_message():

    response = MessagingResponse()
    message = Message()
    userInput = request.values.get('Body', None)
    counter = session.get('counter', 0)
    case = session.get('case', 0)
    mistakes = session.get('mistakes', 0)

    # Start of survey.
    if (counter == 0):
        message.body(welcome)
        session['counter'] = counter + 1
        response.append(message)
        return str(response)

    # Sets the current case based on the user's input.
    # If the user has already selected a case, then
    # the application continues.
    if (not case):
        if (userInput == '1' and counter == 1):
            session['case'] = 1
            case = session.get('case', 0)
        elif (userInput == '2' and counter == 1):
            session['case'] = 2
            case = session.get('case', 0)
        elif (userInput == '3' and counter == 1):
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
            message.body(site_address)
            session['counter'] = counter + 1
        elif (counter == 2):
            if (userInput.upper() == 'RESTART'):
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif (userInput.replace(' ', '').isalnum()):
                cursor.execute(add_site_sql, (userInput,))
                session['row_id'] = cursor.lastrowid
                connection.commit()
                message.body(city)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(site_address_error)
        elif (counter == 3):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_site_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif (userInput.isalpha()):
                cursor.execute(update_site_city_sql, (userInput, session['row_id']))
                connection.commit()
                message.body(zipcode)
                session['counter'] = counter + 1
                session['mistakes'] = 0                
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(city_error)
        elif (counter == 4):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_site_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif (userInput.isdigit() and len(userInput) == 5):
                cursor.execute(update_site_zip_sql, (userInput, session['row_id']))
                connection.commit()
                message.body(in_out)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(zipcode_error)
        elif (counter == 5):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_site_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif userInput == '1':
                cursor.execute(update_site_in_out_sql, (0, session['row_id']))
                connection.commit()
                message.body(dead_or_alive)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            elif userInput == '2':
                cursor.execute(update_site_in_out_sql, (1, session['row_id']))
                connection.commit()
                message.body(dead_or_alive)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(in_out_error)
        elif (counter == 6):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_site_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif userInput == '1':
                cursor.execute(update_site_dead_alive_sql, (0, session['row_id']))
                cursor.execute(update_site_restart_sql, (0, session['row_id']))
                connection.commit()
                session['counter'] = counter + 1
                session['mistakes'] = 0
                message.body(site_picture)
            elif userInput == '2':
                cursor.execute(update_site_dead_alive_sql, (1, session['row_id']))
                cursor.execute(update_site_restart_sql, (0, session['row_id']))
                connection.commit()
                session['counter'] = counter + 1
                session['mistakes'] = 0
                message.body(site_picture)
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(dead_or_alive_error)
        elif (counter == 7):
            # Delete the SQL information as needed
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_site_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif request.values['NumMedia'] != '0':
                filename = request.values['MessageSid'] + '.jpg'
                filepath = IMAGE_DOWNLOAD_DIRECTORY + filename
                with open(filepath, 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
                cursor.execute(update_site_image_sql, (filepath, session['row_id']))
                connection.commit()
                session.clear()
                message.body(survey_complete)
            elif (userInput.upper() == 'DONE'):
                session.clear()
                message.body(survey_complete)   
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(delete_site_sql, (session['row_id'],))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(site_picture_error)

    elif (case == 2):
        if (counter == 1):
            message.body(evidence_address)
            session['counter'] = counter + 1
        elif (counter == 2):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif (userInput.replace(' ', '').isalnum()):
                cursor.execute(add_evidence_sql, (userInput,))
                connection.commit()
                session['row_id'] = cursor.lastrowid
                message.body(city)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(evidence_address_error)
        elif (counter == 3):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif (userInput.isalpha()):
                cursor.execute(update_evidence_city_sql, (userInput, session['row_id']))
                connection.commit()
                message.body(zipcode)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(city_error)
        elif (counter == 4):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif (userInput.isdigit() and len(userInput) == 5):
                cursor.execute(update_evidence_zip_sql, (userInput, session['row_id']))
                connection.commit()
                message.body(category)
                session['counter'] = counter + 1
                session['mistakes'] = 0
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(zipcode_error)
        elif (counter == 5):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif userInput == '1':
                cursor.execute(update_evidence_category_sql, (1, 0, session['row_id']))
                cursor.execute(update_evidence_restart_sql, (0, session['row_id']))
                connection.commit()
                session['counter'] = counter + 1
                session['mistakes'] = 0
                message.body(evidence_picture)
            elif userInput == '2':
                cursor.execute(update_evidence_city_sql, (0, 1, session['row_id']))
                cursor.execute(update_evidence_restart_sql, (0, session['row_id']))
                connection.commit()
                session['counter'] = counter + 1
                session['mistakes'] = 0
                message.body(evidence_picture)
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(category_error)

        elif (counter == 6):
            if (userInput.upper() == 'RESTART'):
                cursor.execute(update_evidence_restart_sql, (1, session['row_id']))
                connection.commit()
                session.clear()
                message.body(restart_prompt)
                response.append(message)
                return str(response)
            elif request.values['NumMedia'] != '0':
                filename = request.values['MessageSid'] + '.jpg'
                filepath = IMAGE_DOWNLOAD_DIRECTORY + filename
                with open(filepath, 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
                cursor.execute(update_evidence_image_sql, (filepath, session['row_id']))
                connection.commit()
                session.clear()
                message.body(survey_complete)
            elif (userInput.upper() == 'DONE'):
                session.clear()
                message.body(survey_complete)   
            else:
                session['mistakes'] = mistakes + 1
                mistakes = session['mistakes']
                if (mistakes == 3):
                    cursor.execute(delete_evidence_sql, (session['row_id'],))
                    connection.commit()
                    session.clear()
                    message.body(mistakes_prompt)
                    response.append(message)
                    return str(response)
                message.body(evidence_picture_error)

    elif (case == 3):
        if (counter == 1):
            message.body(prevention)
            session.clear()

    response.append(message)
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
