
# prompts.py
# Prompt file for RatWatch.

# Prompts for RatWatch survey.

# General prompts.
welcome = ('Welcome to RatWatch! Please reply with one of the following numbers:'
+ '\n  1. I saw a rat \n  2. I saw evidence of a rat'
+ '\n  3. I want to prevent rats\nType \'1\' or \'2\' or \'3\'')

welcome_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please reply with one of the following numbers:'
+ '\n  1. I saw a rat \n  2. I saw evidence of a rat'
+ '\n  3. I want to prevent rats \nType \'1\' or \'2\' or \'3\'')

city = ('Please type the city. For example \'Atlanta\'')

city_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please type the city. For example \'Atlanta\'')

zipcode = ('Please type the zipcode. For example \'30332\'')

zipcode_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please type the zipcode. For example \'30332\'')

survey_complete = ('You have completed the survey. Thank you!')

survey_complete_image = ('Thanks for the image! You have completed the survey.')

# Rat siting prompts.
site_address = ('Where did you see the rat?\n\nType the street name and house number. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

site_address_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the rat?\nType the street name and house number. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

in_out = ('Where did you see the rat? \n 1. Inside \n 2. Outside \nType \'1\' or \'2\'')

in_out_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the rat? \n 1. Inside \n 2.Outside \nType \'1\' or \'2\'')

dead_or_alive = ('Was the rat dead or alive? \n 1. Dead \n 2. Alive \nType \'1\' or \'2\'')

dead_or_alive_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Was the rat dead or alive? \n 1. Dead \n 2. Alive \nType \'1\' or \'2\'')

site_picture = ('Please send us a picture of the rat or where your saw the rat. Otherwise, type \'DONE\' to finish the survey.')

site_picture_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please send us a picture of the rat or where your saw the rat.\nOtherwise, type \'DONE\' to finish the survey.')

# Rat evidence prompts.
evidence_address = ('Where did you see the evidence?\n\nType the street name and house number. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

evidence_address_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Where did you see the evidence?\n\nType the street name and house number. For example \'120 Main Street\' '
+ '\n\nIf you don\'t know the house number, you can just type the street name. For example \'Main Street\'')

category = ('Please categorize your evidence:\n 1. Rat droppings\n 2. Chewed boxes or food \nType \'1\' or \'2\'')

category_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please categorize your evidence:\n 1. Rat droppings\n 2. Chewed boxes or food \nType \'1\' or \'2\'')

evidence_picture = ('Please send us a picture of the evidence. Otherwise, type \'DONE\' to finish the survey.')

evidence_picture_error = ('Your input was incorrect. \nPlease try again. \n\n'
+ 'Please send us a picture of the evidence. Otherwise, type \'DONE\' to end the survey.')

# Interest prompts.
prevention = ('Thank you for your interest in rat prevention. Please follow this link for more info:\nlinkhere')
