# RatWatch

### What is RatWatch?

RatWatch is the text bot that we have developed for members in the community to report real time rat sightings. RatWatch walks the user through a series of questions, collecting vital information which can be presented to the community and community officials. 

RatWatch is built using Python and the Twilio API. MySQL is used for database data storage.

### How to run RatWatch

1. Clone this repository

>Note: For Georgia Tech Civic Data and Design VIP students, please skip step 2 and 3. We already have a payed Twilio account set up for you. Just login and continue with the setup process. Please test if step 4 is needed, you might also be able to skip this step and go on to step 5.

2. Go to the [Twilio website](https://www.twilio.com) and make an account.
3. Get a phone number as the auto-reply number. The free Twilio trial gives you a phone number to use for a couple of months
4. Go to Twilio phone numbers – verified caller IDs, add the phone number you are testing with. This could be your own phone number. Payed twilio account does not require this step.
5. Open terminal, cd to rat-chat directory, type `./ngrok http 5000`
6. Copy the forwarding URL, E.g. https://18565a8e.ngrok.io
7. Go to Twilio phone numbers – active numbers – messaging, paste URL to messaging comes in URL
8. Install MAMP (for mac) or any other local server of your preference. Code in receive_sms uses MAMP and MySQL
9. Database create table code is in the sql directory
10. Make sure you make adjustments to the code so that your code is successfully connected to the database.
11. `python receive_sms.py`

Note: may have to pip install dependencies during this process

12. Your SMS APP should be working now! Have fun gathering data!

# open a terminal window
# cd to ratchat directory
# ./ngrok http 5000
# copy webhook url
# open second terminal window
# cd to ratchat directory
# python receive_sms.py