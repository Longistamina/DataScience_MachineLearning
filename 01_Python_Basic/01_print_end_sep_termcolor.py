#########################
## Single-line print() ##
#########################

print("Hello world!")
print('Hello world!')


######################################
## Multiple-line print() [METHOD 1] ##
######################################

print("""
Immanuel Kant was born in 1724 in Königsberg, Prussia (now Kaliningrad, Russia).\n
He spent his entire life in this city, rarely traveling far from home.\n
He is best known for his work in epistemology, ethics, and aesthetics.
""")

#--------------

print('''
Immanuel Kant's Principle of Universalizability:\n

"Act only according to that maxim whereby you can at the same time will that it should become a universal law."\n

This principle states that before acting,
you should consider whether the rule guiding your action could be applied universally, to everyone, without contradiction.\n

If the action cannot be universalized without causing a contradiction or harm, then it is immoral.
''')


######################################
## Multiple-line print() [METHOD 2] ##
######################################

print(
    (
        "This is the first line."
        "\nThis is the second line."
        "\nThis is the third line."
    )
)
# This is the first line.
# This is the second line.
# This is the third line.


##########################
## print() with "end =" ##
##########################
 
print("Happiness is simple", end = ".")
# Happiness is simple.>>>

print("Happiness is simple", end = " .\n")
# Happiness is simple .
# >>> 


##########################
## print() with "sep =" ##
##########################

print("Happiness", "is", "simple", sep = " - ")
# Happiness - is - simple

print("Happiness", "is", "simple", sep = "|")
# Happiness|is|simple


#------------------------------------------------------------------------------------------------------#
#--------------------------------------- termcolor module ---------------------------------------------#
#------------------------------------------------------------------------------------------------------#

# conda install -c conda-forge termcolor

'''
The termcolor module lets you add ANSI colors and text attributes (bold, underline, etc.) to console output. 

It provides two primary functions:
    # colored(text, color, on_color=None, attrs=None):
    ==> Returns the input string wrapped in ANSI escape codes.

    **cprint(text, color, on_color=None, attrs=None, kwargs):
    ==> Prints colored text directly to the terminal.
'''

from termcolor import colored, cprint

#########################################
## create colored text using colored() ##
## and print it out using print()      ##
#########################################

colored_text = colored(
    text = "This text is so colorful!!!",
    color = "light_cyan",          # color of the text
    on_color = "on_light_red",     # color of the highlight background
    attrs = ["bold", "underline"]  # LIST of text's attributes like "bold", "underline", ... (MUST be a LIST)
)

print(colored_text)


#############################################################
## use RGB tuple to define text color and background color ##
#############################################################

# The RGB value must range from 0-255
# Red:   0 - 255 (256 values)
# Green: 0 - 255 (256 values)
# Blue:  0 - 255 (256 values)
# => In total, we have 256**3 = 16777216 (more than 16.7 million colors)

# So when you want to use colors that are not in the supported list, go search for their RGB values and parse it here like below

text_rgb = (200, 150, 25)

colored_text = colored(
    text = "Which color does this RGB tuple stand for?",
    color = text_rgb,
    on_color = (255, 255, 255), # RGB of white
    attrs = ["blink", "bold"]
)

print(colored_text)


#################################################
## use cprint() to print colored text directly ##
#################################################

green_lantern_oath = '''
   In brightest day, in blackest night, no evil shall escape my sight.     
Let those who worship evil's might, beware my power, Green Lantern's light.
'''

cprint(
    text = green_lantern_oath,
    color = "black",
    on_color = (1,95,64),
    attrs = ['bold']
)


#############################################################
## Combine colored() with Multiple-line print() [METHOD 2] ##
#############################################################

print(
    colored("In brightest day, in blackest night, no evil shall escape my sight.", "green", attrs = ["bold"]),
    colored("\nLet those who worship evil's might, beware my power, Green Lantern's light.", "green", attrs = ["bold"])
)