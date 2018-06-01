
# ratwatch.py: 
# Flask app that interfaces with the Twilio API to create
# an SMS survey for people to report rat sitings or evidence
# in the city of Atlanta. The app also stores user responses
# into a MySQL database for analysis.

import os
import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse

# Establishes a connection with database. Includes
# dictionary with credentials and an exception
# handler in case the connection is unsuccessful.
# Returns cursor for executing statements on the
# database if connection is successful.
def connect_to_database():
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
        return(cursor)
    except mysql.connector.Error:
        raise

cursor = connect_to_database()
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def start_bot():
    case = 0
    counter = 0
    dead_alive_options = {"1": "Dead", "2": "Alive"}
    location_options = {"1": "Inside", "2": "Outside"}
    evidence_options = {"1": "Rat droppings", "2":"Chewed boxes or food"}

    #global var for db
    site_is_outside
    saw_is_alive
    saw_street
    saw_city
    saw_zipcode

    #global var for db evidence of rat
    evid_droppings
    evid_chewed
    evid_street
    evid_city
    evid_zipcode

    response = MessagingResponse()
    message = Message()
    userInput = request.values.get("Body", None)

    #prints what Twilio user texts the bot. Runs each time the user texts.
    print(userInput)

    # ---------- CASE 0: BASE CASE ---------------------------
    # ---------- counter: 0 ---------------
    # ---------- case: 0 -----------------
    if (counter == 0):
        message.body("Hello! Please reply with one of the following numbers:"
        + "\n 1. I saw a rat \n 2. I saw evidence of a rat"
        + "\n 3. I want to prevent rats \n Type '1' or '2' or '3'")
        counter = counter + 1
        response.append(message)
        return str(response)

        #print (counter)
        #print (userInput)
        #print (currCase)
    #------------------- SET CASES --------------------------------
    if (userInput == "1" and counter == 1):
        case = 1
    elif (userInput == "2" and counter == 1):
        case = 2
    elif (userInput == "3" and counter == 1):
        case = 3
    elif (counter == 1):
        message.body("Sorry looks like there was an error."
        + " Please enter only the numbers provided as an option."
        + "\n Type '1' '2' or '3'")
        #reset counters, back to case 0
        # counter = 0
        # case = 0

    #-------------------- CASE LOGIC -----------------------------
    if (case == 1):
        if (counter == 1):
            message.body("Where did you see the rat? \n 1. Inside \n 2.Outside \n Type '1' or '2'")
            counter = counter + 1
            print ("nancytest, should be case1: " + userInput)

        elif (counter == 2 and (userInput == "1" or userInput == "2")):
            message.body("Was the rat dead or alive? \n 1. Dead \n 2. Alive \n Type '1' or '2'")
            counter = counter + 1

            #response for rat sighting: "was the rat inside or outside?"
            print ("nancytest, should be inside/outside: " + dict_location[userInput])

            if userInput == '1':
                saw_is_outside = False
            elif userInput == '2':
                saw_is_outside = True

        elif (counter == 3 and (userInput == "1" or userInput == "2")):
            message.body("Please give us a location. Type the Street Name. For example 'Main Street'")
            counter = counter + 1

            #resonse for rat sighting: "was the rat dead or alive?"
            print ("nancytest, should be alive/dead: " + dict_alive[userInput])

            if userInput == '1':
                saw_is_alive = False
            elif userInput == '2':
                saw_is_alive = True

        elif (counter == 4):
            message.body("Please type the City. For example 'Atlanta'")
            counter = counter + 1

            saw_street = userInput

        elif (counter == 5):
            message.body("Please type the Zipcode. For example '30332'")
            counter = counter + 1

            saw_city = userInput

        elif (counter == 6):
            message.body("Thank you for your response!")
            saw_zipcode = userInput

            addSawRat = "INSERT INTO ratsite (`is_outside`, `is_alive`, `street`, `city`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(addSawRat,(saw_is_outside, saw_is_alive, saw_street, saw_city, saw_zipcode))
            link.commit()

            #resetting the counters, back to case 0
            case = 0
            counter = 0

        else:
            #---------ERROR--------------
            message.body("Sorry looks like there was an error. Please enter only the numbers provided as an option."
            + "\n Type '1' or '2'")
            #reset counters, back to case 0

    elif (case == 2):
        if (counter == 1):
            message.body("Please categorize your evidence:\n 1.Rat Droppings\n 2.Chewed boxes or food \n Type '1' or '2'")
            counter = counter + 1

        elif (counter == 2 and (userInput == "1" or userInput == "2")):
            message.body("Please give us a location. Type the Street Name. For example 'Main Street'")
            counter = counter + 1

            #response for rat evidence: "what type of evidence?"
            print (dict_evidence[userInput])

            if userInput == '1':
                evid_droppings = True
                evid_chewed = False
            elif userInput == '2':
                evid_chewed = True
                evid_droppings = False

        elif (counter == 3):
            message.body("Please type the City. For example 'Atlanta'")
            counter = counter + 1

            evid_street = userInput

        elif (counter == 4):
            message.body("Please type the Zipcode. For example '30332'")
            counter = counter + 1

            evid_city = userInput
            
        elif (counter == 5):
            message.body("Thank you for your response!")

            evid_zipcode = userInput

            #resetting counters, back to case 0
            case = 0
            counter = 0

            addSawEvidence = "INSERT INTO ratevidence (`droppings`, `chewed`, `street`, `city`, `zipcode`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(addSawEvidence,(evid_droppings, evid_chewed, evid_street, evid_city, evid_zipcode))
            link.commit()

        else:
            #-----------ERROR------------
            message.body("Sorry looks like there was an error. Please enter only the numbers provided as an option."
            + "\n Type '1' or '2'")
            #reset counters, back to case 0
            # counter = 0
            # case = 0

    elif (case == 3):
        if (counter == 1):
            message.body("Thank you for your interest in rat prevention. Please follow this link for more info: linkhere")
            counter = 0
            case = 0

    response.append(message)
    return str(response)



if __name__ == "__main__":
    app.run(debug=True)
