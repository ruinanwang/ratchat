
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
sighting_address = ('Question 1 of 4\n\nWhere did you see the rat?\nPlease type the closest address. For example: 559 English Ave NW Atlanta, GA 30318')

sighting_address_error = ('Please make sure you are entering a valid address. Please try again. \n\n'
+ 'Question 1 of 4\n\nWhere did you see the rat?\nPlease type the closest address. For example: 559 English Ave NW Atlanta, GA 30318')

in_out = ('Question 2 of 4\n\nWas the rat inside or outside?\n1. Inside \n2. Outside \nType 1 or 2')

in_out_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Question 2 of 4\n\nWas the rat inside or outside?\n1. Inside \n2. Outside \nType 1 or 2')

dead_or_alive = ('Question 3 of 4\n\nWas the rat dead or alive?\n1. Dead \n2. Alive \nType 1 or 2')

dead_or_alive_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Question 3 of 4\n\nWas the rat dead or alive?\n1. Dead \n2. Alive \nType 1 or 2')

sighting_picture = ('Question 4 of 4\n\nPlease send us a picture of the rat for further analysis. Or, you can type DONE to finish the report.')

sighting_picture_error = ('Please make sure you are sending a valid picture. Please try again. \n\n'
+ 'Question 4 of 4\n\nPlease send us a picture of the rat for further analysis. Or, you can type DONE to finish the report.')

# Rat evidence prompts.
evidence_address = ('Question 1 of 3\n\nWhere did you see the evidence?\nPlease type the closest address. For example: 559 English Ave NW Atlanta, GA 30318')

evidence_address_error = ('Please make sure you are entering a valid house number and street name. Please try again. \n\n'
+ 'Question 1 of 3\n\nWhere did you see the evidence?\nPlease type the closest address. For example: 559 English Ave NW Atlanta, GA 30318')

category = ('Question 2 of 3\n\nWhat kind of evidence did you find?\n1. Rat droppings\n2. Chewed things \nType 1 or 2')

category_error = ('Please make sure you are entering a valid number. Please try again. \n\n'
+ 'Question 2 of 3\n\nWhat kind of evidence did you find?\n1. Rat droppings\n2. Chewed things\nType 1 or 2')

evidence_picture = ('Question 3 of 3\n\nPlease send us a picture of the evidence for further analysis. Or, you can type DONE to finish the report.')

evidence_picture_error = ('Please make sure you are sending a valid picture. Please try again. \n\n'
+ 'Question 3 of 3\n\nPlease send us a picture of the evidence for further analysis. Or, you can type DONE to end the report.')

# Interest prompts.
prevention_prompt = ('Thank you for your interest in rat prevention. Here are some tips on how to prevent rats: \n\n'
+ '1. Seal any holes in your house with caulk\n2. Store food and trash in bins with tight-fitting lids\n3. Report '
+ 'illegal dumping to 311\n\nTo view your options again, please type RAT.')
