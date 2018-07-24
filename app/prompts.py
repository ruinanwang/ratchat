
# prompts.py
# Prompt file for RatWatch.

# Prompts for RatWatch report.

# General prompts.

address = ('Welcome to RatWatch!'
+ ' Please text the closest address'
+ ' to where you saw the rat/evidence.')

address_image = ('Welcome to RatWatch and'
+ ' thanks for the image! Please text the'
+ ' closest address to where you saw the'
+ ' rat/evidence.')

too_many_images = ('Welcome to RatWatch!'
+ ' Unfortunately, we can only process one'
+ ' image per report. Please only text one'
+ ' image for each report you make. Thank you!')

address_error = ('Sorry, we didn\'t recognize that'
+ ' address. Please double check it to make sure it\'s'
+ ' right and text it again. If you\'re sure it\'s right,'
+ ' text YES.')

partial_address = ('Please make sure you are texting'
+ ' a house number and street name. We need this'
+ ' information to accurately locate the rat/evidence.' 
+ ' Please try again.')

options = ('Great! Now just text one of the letters next'
+ ' to the description of what you found/saw:\n\n'
+ ' A = Saw a live rat outside\n'
+ ' B = Saw a live rat inside\n'
+ ' C = Saw a dead rat outside\n'
+ ' D = Saw a dead rat inside\n'
+ ' E = Found chewed things\n'
+ ' F = Found droppings\n'
+ ' G = Found a rat hole')

option_error = ('Please make sure you are texting a' 
+ ' valid letter. Please try again.')

done = ('Done! Thanks for your response!'
+ ' If you would like to make another report,' 
+ ' text an image or text RAT.')

mistakes = ('You made too many mistakes,'
+ ' so we had to end your report. To make another'
+ ' report, please text an image or text RAT.')








