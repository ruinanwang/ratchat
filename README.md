# RatWatch

RatWatch is an SMS chatbot designed for members in the Atlanta community to report rat sightings and evidence. RatWatch lets you fill out a simple survey in order to collect vital information which can be presented to the community and city officials.

RatWatch is built using Python, Flask, MySQL, and Twilio.

## How to Run RatWatch

### Getting Started

1. Clone this repository.
2. Go to the [Twilio website](https://www.twilio.com) and make an account.
3. Get a phone number as the auto-reply number. The free Twilio trial gives you a phone number to use for a couple of months.
4. Go to Twilio phone numbers – verified caller IDs and add the phone number you are testing with. This could be your own phone number. A paid Twilio account does not require this step.
5. Open terminal, cd to ratchat/app directory, type `./ngrok http 5000`, and hit enter.
6. Copy the URL that appears in the terminal, E.g. https://18565a8e.ngrok.io
7. Go to Twilio phone numbers – active numbers and click on the phone number you set up. Then, under "Messaging," paste the forwarding URL into the "a message comes in" section. Make sure you select "Webhook" in the dropdown menu and "HTTP GET."
8. Click "Save" at the bottom of the screen to save your changes.

### Creating the Virtual Environment
1. cd into the ratchat directory.
2. Type `virtualenv venv` in the terminal and hit enter.
3. Activate the virtual environment by typing `source venv/bin/activate` and hitting enter.
4. Type `pip install -r requirements.txt` in the terminal and hit enter to install the necessary packages for the project.

### Running the App
1. Install [MAMP](https://www.mamp.info/en/downloads/).
2. Start the MAMP server and navigate to the phpMyAdmin page.
3. Copy the `ratwatch_db.sql` code and execute it on the MAMP server in order to create the database.
4. Change the name of the configuration file to "config.py" and change the values to match your local setup.
5. Type `python __init__.py` in the terminal and hit enter.
    
Your SMS APP should be working now! Just text the phone number or visit localhost:5000 in your browser to get started! Have fun gathering data!

## How to run Unit Tests
Unit tests are really great for making sure the app works. We wrote some unit tests for this project to do just that! To run the tests, just cd into the ratchat/app directory and type `python -m unittest discover -v`. Then hit enter.

A list of all the tests will appear in the terminal, and you will see if any of them failed. This will help a lot if you want to find errors in the code.