
# prompts.py
# Prompt file for RatWatch.

# Prompts for RatWatch survey.

# General prompts.
welcome = ('Welcome to RatWatch!'
+ '\n1. I saw a rat \n2. I saw evidence of a rat'
+ '\n3. I want to prevent rats'
+ '\nType 1, 2, or 3'
+ '\n\nIf you need to restart the survey at any point, just type RESTART')

welcome_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Welcome to RatWatch!'
+ '\n1. I saw a rat \n2. I saw evidence of a rat'
+ '\n3. I want to prevent rats'
+ '\nType 1, 2, or 3')

city = ('Please type the city. For example: Atlanta')

city_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please type the city. For example: Atlanta')

zipcode = ('Please type the ZIP code. For example: 30332')

zipcode_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please type the ZIP code. For example: 30332')

survey_complete = ('You have completed the survey. Thank you for your response! Just text us again if you want to make another report :)')

mistakes_prompt = ('You have made too many errors on the survey. Your report was not saved. To restart, please text us again.')

restart_prompt = ('You have restarted the survey. To make a new report, please text us again.')

# Rat siting prompts.
site_address = ('Where did you see the rat?\n\nType the house number and street name. For example: 120 Main Street'
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example: Main Street')

site_address_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the rat?\nType the house number and street name. For example: 120 Main Street'
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example: Main Street')

in_out = ('Was the rat inside or outside?\n1. Inside \n2. Outside \nType 1 or 2')

in_out_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Was the rat inside or outside?\n1. Inside \n2. Outside \nType 1 or 2')

dead_or_alive = ('Was the rat dead or alive?\n1. Dead \n2. Alive \nType 1 or 2')

dead_or_alive_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Was the rat dead or alive?\n1. Dead \n2. Alive \nType 1 or 2 ')

site_picture = ('Please send us a picture of the rat or where your saw the rat. Or, you can type DONE to finish the survey.')

site_picture_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please send us a picture of the rat or where your saw the rat. Or, you can type DONE to finish the survey.')

# Rat evidence prompts.
evidence_address = ('Where did you see the evidence?\n\nType the house number and street name. For example: 120 Main Street'
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example: Main Street')

evidence_address_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the evidence?\n\nType the house number and street name. For example: 120 Main Street'
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example: Main Street')

category = ('What kind of evidence did you find?\n1. Rat droppings\n2. Chewed things \nType 1 or 2')

category_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'What kind of evidence did you find?\n1. Rat droppings\n2. Chewed things\nType 1 or 2')

evidence_picture = ('Please send us a picture of the evidence. Or, you can type DONE to finish the survey.')

evidence_picture_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please send us a picture of the evidence. Or, you can type DONE to end the survey.')

# Interest prompts.
prevention = ('Thank you for your interest in rat prevention. Please follow this link for more info:\nlinkhere')
