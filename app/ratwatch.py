
# ratwatch.py: 
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
survey_complete_image = prompts.survey_complete_image

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

# SQL statements for inserting and updating information.
addSiteSQL = config.addSiteSQL
addEvidenceSQL = config.addEvidenceSQL
updateSiteImageSQL = config.updateSiteImageSQL
updateEvidenceImageSQL = config.updateEvidenceImageSQL

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

    # Case 0 - Start
    if (counter == 0):
        message.body(welcome)
        counter += 1
        session['counter'] = counter
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
            message.body(welcome_error)

    # Decision tree that carries out the appropriate 
    # logic based on the case and the counter.
    if (case == 1):
        if (counter == 1):
            message.body(site_address)
            counter += 1         
            session['counter'] = counter
        elif (counter == 2):
            if (userInput.replace(' ', '').isalnum()):
                session['site_street'] = userInput
                message.body(city)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(site_address_error)
        elif (counter == 3):
            if (userInput.isalpha()):
                session['site_city'] = userInput
                message.body(zipcode)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(city_error)
        elif (counter == 4):
            if (userInput.isdigit() and len(userInput) == 5):
                session['site_zipcode'] = userInput
                message.body(in_out)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(zipcode_error)
        elif (counter == 5):
            if userInput == '1':
                session['site_is_outside'] = False
                message.body(dead_or_alive)
                counter += 1         
                session['counter'] = counter
            elif userInput == '2':
                session['site_is_outside'] = True
                message.body(dead_or_alive)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(in_out_error)
        elif (counter == 6):
            if userInput == '1':
                session['site_is_alive'] = False
                site_is_outside = session.get('site_is_outside', 0)
                site_is_alive = session.get('site_is_alive', 0)
                site_street = session.get('site_street', 0)
                site_city = session.get('site_city', 0)
                site_zipcode = session.get('site_zipcode', 0)

                cursor.execute(addSiteSQL,(site_is_outside, site_is_alive, site_street, site_city, site_zipcode))
                session['rowId'] = cursor.lastrowid
                connection.commit()
                counter += 1
                session['counter'] = counter
                message.body(site_picture)
            elif userInput == '2':
                session['site_is_alive'] = True
                site_is_outside = session.get('site_is_outside', 0)
                site_is_alive = session.get('site_is_alive', 0)
                site_street = session.get('site_street', 0)
                site_city = session.get('site_city', 0)
                site_zipcode = session.get('site_zipcode', 0)

                cursor.execute(addSiteSQL,(site_is_outside, site_is_alive, site_street, site_city, site_zipcode))
                session['rowId'] = cursor.lastrowid
                connection.commit()
                counter += 1
                session['counter'] = counter
                message.body(site_picture)
            else:
                message.body(dead_or_alive_error)
        elif (counter == 7):
            if request.values['NumMedia'] != '0':
                filename = request.values['MessageSid'] + '.png'
                filepath = IMAGE_DOWNLOAD_DIRECTORY + filename
                with open(filepath, 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
                cursor.execute(updateSiteImageSQL, (filepath, session['rowId']))
                connection.commit()
                session.clear()
                message.body(survey_complete_image)
            elif (userInput.upper() == 'DONE'):
                session.clear()
                message.body(survey_complete)   
            else:
                message.body(site_picture_error)

    elif (case == 2):
        if (counter == 1):
            message.body(evidence_address)
            counter += 1         
            session['counter'] = counter
        elif (counter == 2):
            if (userInput.replace(' ', '').isalnum()):
                session['evidence_street'] = userInput
                message.body(city)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(evidence_address_error)
        elif (counter == 3):
            if (userInput.isalpha()):
                session['evidence_city'] = userInput
                message.body(zipcode)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(city_error)
        elif (counter == 4):
            if (userInput.isdigit() and len(userInput) == 5):
                session['evidence_zipcode'] = userInput
                message.body(category)
                counter += 1         
                session['counter'] = counter
            else:
                message.body(zipcode_error)
        elif (counter == 5):
            if userInput == '1':
                session['evidence_droppings'] = True
                session['evidence_chewed'] = False

                evidence_droppings = session.get('evidence_droppings', 0)
                evidence_chewed = session.get('evidence_chewed', 0)
                evidence_street = session.get('evidence_street', 0)
                evidence_city = session.get('evidence_city', 0)
                evidence_zipcode = session.get('evidence_zipcode', 0)

                cursor.execute(addEvidenceSQL,(evidence_droppings, evidence_chewed, evidence_street, evidence_city, evidence_zipcode))                
                session['rowId'] = cursor.lastrowid
                connection.commit()
                counter += 1
                session['counter'] = counter
                message.body(evidence_picture)
            elif userInput == '2':
                session['evidence_droppings'] = False
                session['evidence_chewed'] = True

                evidence_droppings = session.get('evidence_droppings', 0)
                evidence_chewed = session.get('evidence_chewed', 0)
                evidence_street = session.get('evidence_street', 0)
                evidence_city = session.get('evidence_city', 0)
                evidence_zipcode = session.get('evidence_zipcode', 0)

                cursor.execute(addEvidenceSQL,(evidence_droppings, evidence_chewed, evidence_street, evidence_city, evidence_zipcode))
                session['rowId'] = cursor.lastrowid
                connection.commit()
                counter += 1
                session['counter'] = counter
                message.body(evidence_picture)
            else:
                message.body(category_error)

        elif (counter == 6):
            if request.values['NumMedia'] != '0':
                filename = request.values['MessageSid'] + '.png'
                filepath = IMAGE_DOWNLOAD_DIRECTORY + filename
                with open(filepath, 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
                cursor.execute(updateEvidenceImageSQL, (filepath, session['rowId']))
                connection.commit()
                session.clear()
                message.body(survey_complete_image)
            elif (userInput.upper() == 'DONE'):
                session.clear()
                message.body(survey_complete)   
            else:
                message.body(evidence_picture_error)

    elif (case == 3):
        if (counter == 1):
            message.body(prevention)
            session.clear()

    response.append(message)
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
