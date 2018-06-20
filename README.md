# RatWatch

### What is RatWatch?

RatWatch is a SMS chatbot designed for members in the Atlanta community to report real-time rat sightings. RatWatch walks the user through a series of questions, collecting vital information which can be presented to the community and city officials. 

RatWatch is built using Python and Twilio. MySQL is used for database storage.

### How to run RatWatch

1. Clone this repository

>Note: For Georgia Tech Civic Data and Design VIP students, please skip step 2 and 3. We already have a paid Twilio account set up for you. Just login and continue with the setup process. Please test if step 4 is needed. You might also be able to skip this step and go on to step 5.

1. Go to the [Twilio website](https://www.twilio.com) and make an account
2. Get a phone number as the auto-reply number. The free Twilio trial gives you a phone number to use for a couple of months
3. Go to Twilio phone numbers – verified caller IDs, add the phone number you are testing with. This could be your own phone number. Paid twilio account does not require this step
4. Open terminal, cd to ratchat directory, type `./ngrok http 5000`
5. Copy the forwarding URL that appears in the terminal, E.g. https://18565a8e.ngrok.io
6. Go to Twilio phone numbers – active numbers, and click on the phone number you set up. Then, under "Messaging," paste the the forwarding URL into the "a message comes in" section. Make sure you select "Webhook" in the dropdown menu and "HTTP GET"
7. Install MAMP (Mac) or XAMPP (Windows) any other local server of your preference.
8. Run the SQL code in the database folder on your server in order to create the database.
9. Make adjustments to the configuration file so that 
10. `python __init__.py`

Note: may have to pip install dependencies during this process.

Your SMS APP should be working now! Have fun gathering data!