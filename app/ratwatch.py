
# ratwatch.py: 
# Flask app that interfaces with the Twilio API to create
# an SMS survey for people to report rat sitings or evidence
# in the city of Atlanta. The app also stores user responses
# into a MySQL database for analysis.
# - Michael Koohang

import os
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, session
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

# Function that establishes a connection with database. 
# Includes dictionary with credentials and an exception
# handler in case the connection is unsuccessful.
# Returns cursor for executing statements on the
# database if connection is successful.
# - Michael Koohang
try:
    databaseCredentials = {
        'user': 'root',
        'password': 'root',
        'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
        'database': 'ratwatch_db',
        'raise_on_warnings': True,
    }
    link = mysql.connector.connect(**databaseCredentials)
    cursor = link.cursor()
except mysql.connector.Error:
    raise

# Initiates connection with the database and 
# starts the application.
# - Michael Koohang
SECRET_KEY = 'al;kasd7jkhdtr4576576lkjasrt'
app = Flask(__name__)
app.config.from_object(__name__)

# Function that executes when the user
# texts the phone number and the Twilio
# API is activated.
# - Michael Koohang
@app.route("/sms", methods=['GET', 'POST'])
def process_message():

    response = MessagingResponse()
    message = Message()
    userInput = request.values.get("Body", None)
    counter = session.get('counter', 0)
    case = session.get('case', 0)

    # Prints what the user texts the chatbot. It runs each 
    # time the user sends a message.
    # - Michael Koohang
    print(userInput)

    # Case 0 - Start
    # - Michael Koohang
    if (counter == 0):
        message.body("Welcome to RatWatch! Please reply with one of the following numbers:"
        + "\n 1. I saw a rat \n 2. I saw evidence of a rat"
        + "\n 3. I want to prevent rats \n Type '1' or '2' or '3'")
        counter += 1
        session['counter'] = counter
        response.append(message)
        return str(response)

    # Determines which option the user selected and sets
    # the current case based on that.
    # - Michael Koohang
    if (not case):
        if (userInput == "1" and counter == 1):
            session['case'] = 1
            case = session.get('case', 0)
        elif (userInput == "2" and counter == 1):
            session['case'] = 2
            case = session.get('case', 0)
        elif (userInput == "3" and counter == 1):
            session['case'] = 3
            case = session.get('case', 0)
        else:
            message.body("Your input was incorrect. \nPlease try again. \n\n"
            + "Please reply with one of the following numbers:"
            + "\n 1. I saw a rat \n 2. I saw evidence of a rat"
            + "\n 3. I want to prevent rats \n Type '1' or '2' or '3'")

    # Decision tree that carries out the appropriate 
    # logic based on the case and the counter.
    # - Michael Koohang
    if (case == 1):
        if (counter == 1):
            message.body("Where did you see the rat?. Type the street name. For example '120 Main Street'")
            counter += 1         
            session['counter'] = counter
        elif (counter == 2):
            if (userInput.replace(' ','').isalnum()):
                session['site_street'] = userInput
                message.body("Please type the City. For example 'Atlanta'")
                counter += 1         
                session['counter'] = counter
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Where did you see the rat?. Type the street name. For example '120 Main Street'")
        elif (counter == 3):
            if (userInput.isalpha()):
                session['site_city'] = userInput
                message.body("Please type the Zipcode. For example '30332'")
                counter += 1         
                session['counter'] = counter
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Please type the City. For example 'Atlanta'")
        elif (counter == 4):
            try:
                userInput = int(userInput)
                session['site_zipcode'] = userInput
                message.body("Where did you see the rat? \n 1. Inside \n 2.Outside \n Type '1' or '2'")
                counter += 1         
                session['counter'] = counter
            except:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Please type the Zipcode. For example '30332'")
        elif (counter == 5):
            if userInput == '1':
                session['site_is_outside'] = False
                message.body("Was the rat dead or alive? \n 1. Dead \n 2. Alive \n Type '1' or '2'")
                counter += 1         
                session['counter'] = counter
            elif userInput == '2':
                session['site_is_outside'] = True
                message.body("Was the rat dead or alive? \n 1. Dead \n 2. Alive \n Type '1' or '2'")
                counter += 1         
                session['counter'] = counter
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Where did you see the rat? \n 1. Inside \n 2.Outside \n Type '1' or '2'")
        elif (counter == 6):
            if userInput == '1':
                session['site_is_alive'] = False
                site_is_outside = session.get('site_is_outside', 0)
                site_is_alive = session.get('site_is_alive', 0)
                site_street = session.get('site_street', 0)
                site_city = session.get('site_city', 0)
                site_zipcode = session.get('site_zipcode', 0)

                addSite = "INSERT INTO ratsite (`is_outside`, `is_alive`, `street`, `city`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(addSite,(site_is_outside, site_is_alive, site_street, site_city, site_zipcode))
                link.commit()
                session.clear()
                message.body("Thank you for your response!")
            elif userInput == '2':
                session['site_is_alive'] = True
                site_is_outside = session.get('site_is_outside', 0)
                site_is_alive = session.get('site_is_alive', 0)
                site_street = session.get('site_street', 0)
                site_city = session.get('site_city', 0)
                site_zipcode = session.get('site_zipcode', 0)

                addSite = "INSERT INTO ratsite (`is_outside`, `is_alive`, `street`, `city`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(addSite,(site_is_outside, site_is_alive, site_street, site_city, site_zipcode))
                link.commit()
                session.clear()
                message.body("Thank you for your response!")
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Was the rat dead or alive? \n 1. Dead \n 2. Alive \n Type '1' or '2'")

        # Implement image feature here.

    elif (case == 2):
        if (counter == 1):
            message.body("Where did you see the evidence? Type the street name. For example '120 Main Street'")
            counter += 1         
            session['counter'] = counter
        elif (counter == 2):
            if (userInput.replace(' ','').isalnum()):
                session['evidence_street'] = userInput
                message.body("Please type the City. For example 'Atlanta'")
                counter += 1         
                session['counter'] = counter
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Where did you see the evidence?. Type the street name. For example '120 Main Street'")
        elif (counter == 3):
            if (userInput.isalpha()):
                session['evidence_city'] = userInput
                message.body("Please type the Zipcode. For example '30332'")
                counter += 1         
                session['counter'] = counter
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Please type the City. For example 'Atlanta'")
        elif (counter == 4):
            try:
                userInput = int(userInput)
                session['evidence_zipcode'] = userInput
                message.body("Please categorize your evidence:\n 1.Rat Droppings\n 2.Chewed boxes or food \n Type '1' or '2'")
                counter += 1         
                session['counter'] = counter
            except:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Please type the Zipcode. For example '30332'")
        elif (counter == 5):
            if userInput == '1':
                session['evidence_droppings'] = True
                session['evidence_chewed'] = False

                evidence_droppings = session.get('evidence_droppings', 0)
                evidence_chewed = session.get('evidence_chewed', 0)
                evidence_street = session.get('evidence_street', 0)
                evidence_city = session.get('evidence_city', 0)
                evidence_zipcode = session.get('evidence_zipcode', 0)

                addEvidence = "INSERT INTO ratevidence (`droppings`, `chewed`, `street`, `city`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(addEvidence,(evidence_droppings, evidence_chewed, evidence_street, evidence_city, evidence_zipcode))
                link.commit()
                session.clear()
                message.body("Thank you for your response!")
            elif userInput == '2':
                session['evidence_chewed'] = True
                session['evidence_droppings'] = False

                evidence_droppings = session.get('evidence_droppings', 0)
                evidence_chewed = session.get('evidence_chewed', 0)
                evidence_street = session.get('evidence_street', 0)
                evidence_city = session.get('evidence_city', 0)
                evidence_zipcode = session.get('evidence_zipcode', 0)

                addEvidence = "INSERT INTO ratevidence (`droppings`, `chewed`, `street`, `city`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(addEvidence,(evidence_droppings, evidence_chewed, evidence_street, evidence_city, evidence_zipcode))
                link.commit()
                session.clear()
                message.body("Thank you for your response!")
            else:
                message.body("Your input was incorrect. \nPlease try again. \n\n"
                + "Please categorize your evidence:\n 1.Rat Droppings\n 2.Chewed boxes or food \n Type '1' or '2'")

        # Implement image feature here.

    elif (case == 3):
        if (counter == 1):
            message.body("Thank you for your interest in rat prevention. Please follow this link for more info: linkhere")
            session.clear()

    response.append(message)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
