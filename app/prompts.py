
# prompts.py
# Prompt file for RatWatch.

# Prompts for RatWatch report.

# General prompts.
welcome = ('Welcome to RatWatch!'
+ '\n\n1. I saw a rat \n2. I saw evidence of a rat'
+ '\n3. I want more information on how to prevent rats'
+ '\nType 1, 2, or 3'
+ '\n\nIf you make any mistakes, you can restart the report by typing RESTART')

welcome_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Welcome to RatWatch!'
+ '\n\n1. I saw a rat \n2. I saw evidence of a rat'
+ '\n3. I want more information on how to prevent rats'
+ '\nType 1, 2, or 3'
+ '\n\nIf you make any mistakes, you can restart the report by typing RESTART')

report_complete = ('You have completed the report. Thank you for your response! If you would like to make another report, please type RAT.')

mistakes_prompt = ('You made too many mistakes, so we had to restart your report. To make another report, please type RAT.')

# Rat sighting prompts.
sighting_address = ('Question 1 of 6\n\nWhere did you see the rat?\nPlease type the closest house number and street name. For example: 120 Main St')

sighting_address_error = ('Please make sure you are entering a valid house number and street name. Please try again. \n\n'
+ 'Question 1 of 6\n\nWhere did you see the rat?\nPlease type the closest house number and street name. For example: 120 Main St')

sighting_city = ('Question 2 of 6\n\nPlease type the city. For example: Atlanta')

sighting_city_error = ('Please make sure you are entering a valid city. Please try again. \n\n'
+ 'Question 2 of 6\n\nPlease type the city. For example: Atlanta')

sighting_zipcode = ('Question 3 of 6\n\nPlease type the ZIP code. For example: 30332')

sighting_zipcode_error = ('Please make sure you are entering a valid ZIP code. Please try again. \n\n'
+ 'Question 3 of 6\n\nPlease type the ZIP code. For example: 30332')

in_out = ('Question 4 of 6\n\nWas the rat inside or outside?\n1. Inside \n2. Outside \nType 1 or 2')

in_out_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Question 4 of 6\n\nWas the rat inside or outside?\n1. Inside \n2. Outside \nType 1 or 2')

dead_or_alive = ('Question 5 of 6\n\nWas the rat dead or alive?\n1. Dead \n2. Alive \nType 1 or 2')

dead_or_alive_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Question 5 of 6\n\nWas the rat dead or alive?\n1. Dead \n2. Alive \nType 1 or 2 ')

sighting_picture = ('Question 6 of 6\n\nPlease send us a picture of the rat for further analysis. Or, you can type DONE to finish the report.')

sighting_picture_error = ('Please make sure you are sending a valid picture. Please try again. \n\n'
+ 'Question 6 of 6\n\nPlease send us a picture of the rat for further analysis. Or, you can type DONE to finish the report.')

# Rat evidence prompts.
evidence_address = ('Question 1 of 5\n\nWhere did you see the evidence?\nPlease type the closest house number and street name. For example: 120 Main St')

evidence_address_error = ('Please make sure you are entering a valid house number and street name. Please try again. \n\n'
+ 'Question 1 of 5\n\nWhere did you see the evidence?\nPlease type the closest house number and street name. For example: 120 Main St')

evidence_city = ('Question 2 of 5\n\nPlease type the city. For example: Atlanta')

evidence_city_error = ('Please make sure you are entering a valid city. Please try again. \n\n'
+ 'Question 2 of 5\n\nPlease type the city. For example: Atlanta')

evidence_zipcode = ('Question 3 of 5\n\nPlease type the ZIP code. For example: 30332')

evidence_zipcode_error = ('Please make sure you are entering a valid ZIP code. Please try again. \n\n'
+ 'Question 3 of 5\n\nPlease type the ZIP code. For example: 30332')

category = ('Question 4 of 5\n\nWhat kind of evidence did you find?\n1. Rat droppings\n2. Chewed things \nType 1 or 2')

category_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Question 4 of 5\n\nWhat kind of evidence did you find?\n1. Rat droppings\n2. Chewed things\nType 1 or 2')

evidence_picture = ('Question 5 of 5\n\nPlease send us a picture of the evidence for further analysis. Or, you can type DONE to finish the report.')

evidence_picture_error = ('Please make sure you are sending a valid picture. Please try again. \n\n'
+ 'Question 5 of 5\n\nPlease send us a picture of the evidence for further analysis. Or, you can type DONE to end the report.')

# Interest prompts.
prevention_prompt = ('Thank you for your interest in rat prevention. Here are some tips on how to prevent rats: \n\n'
+ '1. Seal any holes in your house with caulk\n2. Store food and trash in bins with tight-fitting lids\n3. Report '
+ 'illegal dumping to 311\n\nTo view your options again, please type RAT.')
