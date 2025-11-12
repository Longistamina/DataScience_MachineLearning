#########################
## Single-line print() ##
#########################

print("Hello world!")
print('Hello world!')


######################################
## Multiple-line print() [METHOD 1] ##
######################################

print("""
Sir Isaac Newton was born on January 4, 1643, in Woolsthorpe, England.

He was a physicist, mathematician, astronomer, and author 
who is widely recognized as one of the most influential scientists of all time.
      
Two his greatest contributions to science are:
+ The 3 laws of motion
+ The invention of calculus (integral and differential calculus)
""")

#--------------

print('''
Sir Isaac Newton, a devout Christian, had a close friend who was an atheist. 
One day, Newton invited him over to his study. 
As the friend entered, he noticed a beautifully crafted model of the solar system—made of gold and other fine materials. 
The planets were positioned accurately and moved in perfect harmony.\n

Amazed, the friend asked, “This is incredible! Who made it?"
Newton calmly replied, “No one. It just formed itself—particles randomly came together to create it.”
The friend laughed and said, “Come on, that's impossible. Someone clearly designed and built this!”\n

Newton looked at him and said, “If you can't believe that this small model came about by chance, 
then how can you believe that the real solar system, infinitely more complex and vast, 
came into existence without a Creator?"
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