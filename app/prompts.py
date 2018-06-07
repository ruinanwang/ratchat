
# prompts.py
# Prompt file for RatWatch.

# Prompts for RatWatch survey.

# General prompts.
welcome = ('Welcome to RatWatch! Type \'1\' or \'2\' or \'3\''
+ '\n  1. I saw a rat \n  2. I saw evidence of a rat'
+ '\n  3. I want to prevent rats')

welcome_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Type \'1\' or \'2\' or \'3\''
+ '\n  1. I saw a rat \n  2. I saw evidence of a rat'
+ '\n  3. I want to prevent rats \n')

city = ('Please type the city. For example \'Atlanta\'')

city_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please type the city. For example \'Atlanta\'')

zipcode = ('Please type the ZIP code. For example \'30332\'')

zipcode_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please type the ZIP code. For example \'30332\'')

survey_complete = ('You have completed the survey. Thank you for your response! Just text us again if you want to make another report :)')

mistakes_prompt = ('You have made too many errors on the survey. To restart, please text us again.')

restart = ('If you would like to restart the survey, just type \'RESTART\'')

# Rat siting prompts.
site_address = ('Where did you see the rat?\n\nType the house number and street name. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

site_address_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the rat?\nType the house number and street name. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

in_out = ('Was the rat inside or outside?\nType \'1\' or \'2\' \n 1. Inside \n 2. Outside ')

in_out_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Was the rat inside or outside?\nType \'1\' or \'2\' \n 1. Inside \n 2. Outside ')

dead_or_alive = ('Was the rat dead or alive?\nType \'1\' or \'2\' \n 1. Dead \n 2. Alive ')

dead_or_alive_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Was the rat dead or alive?\nType \'1\' or \'2\' \n 1. Dead \n 2. Alive ')

site_picture = ('Please send us a picture of the rat or where your saw the rat. Or, you can type \'DONE\' to finish the survey.')

site_picture_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please send us a picture of the rat or where your saw the rat. Or, you can type \'DONE\' to finish the survey.')

# Rat evidence prompts.
evidence_address = ('Where did you see the evidence?\n\nType the house number and street name. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

evidence_address_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the evidence?\n\nType the house number and street name. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

category = ('What kind of evidence did you find?\nType \'1\' or \'2\'\n 1. Rat droppings\n 2. Chewed boxes or food ')

category_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'What kind of evidence did you find?\nType \'1\' or \'2\'\n 1. Rat droppings\n 2. Chewed boxes or food')

evidence_picture = ('Please send us a picture of the evidence. Or, you can type \'DONE\' to finish the survey.')

evidence_picture_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please send us a picture of the evidence. Or, you can type \'DONE\' to end the survey.')

# Interest prompts.
prevention = ('Thank you for your interest in rat prevention. Please follow this link for more info:\nlinkhere')
