'''
ArgumentParser is Python's built-in solution for creating powerful command-line interfaces (CLIs).

It's part of the argparse module, which comes pre-installed with Python 
and makes it easy to write user-friendly command-line programs.

ArgumentParser automatically generates help messages, handles errors when users provide invalid arguments, 
and supports both positional and optional arguments.
'''

##########################

'''
The Three-Step Process
1. Create the parser: parser = argparse.ArgumentParser()
2. Add arguments: parser.add_argument()
3. Parse arguments: args = parser.parse_args()
'''

##########################

'''
| Parameter       | Type  | Description                         | Default                 |
|-----------------|-------|-------------------------------------|-------------------------|
| prog            | str   | Program name (shown in help)        | sys.argv                |
| description     | str   | Text displayed before argument help | None                    |
| epilog          | str   | Text displayed after argument help  | None                    |
| usage           | str   | Custom usage message                | Generated automatically |
| formatter_class | class | Class for customizing help output   | HelpFormatter           |
| add_help        | bool  | Add -h/--help option                | True                    |
| allow_abbrev    | bool  | Allow abbreviation of long options  | True                    |
'''


#----------------------------------------------------------------------------------------------------------#
#--------------------------------- Define functional functions --------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

from loguru import logger
from pathlib import Path

def rectangle_perimeter(length, width):
    """Calculate the perimeter of a rectangle."""
    try:
        length = float(length)  # Ensure length is a float
        width = float(width)   # Ensure width is a float
        assert length > 0 and width > 0, "Length and width must be positive numbers."
    except ValueError as ve:
        logger.error(f"Invalid input: {ve}. Length and width must be numbers.")
        return None
    except AssertionError as ae:
        logger.error(ae)
        return None
    else:
        return 2 * (length + width)


def rectangle_area(length, width):
    """Calculate the area of a rectangle."""
    # Don't need to check the length and width's constrains, since the perimeter function has already done that
    length = float(length)
    width = float(width)
    return length * width


def save_results(out_message, filepath):
    """Save the results to a file."""
    if filepath == "": # The user don't want to save the results
        return None  
    elif Path(filepath).suffix == "": # The user didn't provide a file extension
        logger.error(f"The {filepath} is not a file.") 
        return None 
    else:
        with open(filepath, 'w') as file: # Save the results to the specified file
            file.write(out_message)
        logger.info(f"Results saved to {filepath}")


#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------ Create ArgumentParser object --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

from argparse import ArgumentParser, HelpFormatter

# Custom formatter with increased width and max help position
formatter = lambda prog: HelpFormatter(prog, width=200, max_help_position=50)

# Put the parser inside a function so that it will not be executed when the module is imported
def parse_args():
    # Create an ArgumentParser object named "parser"
    parser = ArgumentParser(prog = "Rectangle Calculator",
                            description = "Calculate the perimeter and area of a rectangle.",
                            epilog = "Thank you for using the Rectangle Calculator!",
                            usage = "rectangle_calculator.py [options] <length> <width>",
                            add_help = True,
                            formatter_class = formatter)

    # Add arguments to the "parser" object
    parser.add_argument("-l", "--length", required=True, metavar="\b", help="Length of the rectangle (expected to be a positive number).")
    parser.add_argument("-w", "--width", required=True, metavar="\b", help="Width of the rectangle (expected to be a positive number).")
    parser.add_argument("-o", "--out", required=False, metavar="\b", type=str, default="", help="Path to the output file saving the results.")

    return parser.parse_args()  # Parse the command-line arguments and return them

# -o means short flag
# --out means long flag
# required = True means that the argument is mandatory (False means optional)
# metavar = "\b" to hide the metavar like LENGTH and WIDTH, and avoid the space character like "-l , --length" (if set metavar="")
# type = str means that the argument MUST be a string
# default = "" means that if the user doesn't provide this argument, an empty string will be parsed as default value
# help = "..." is the description of the argument that will be shown in the help message


#--------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------- Define main() function ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

def main():
    try:
        # Parse the command-line arguments given by the user
        args = parse_args() 

        # Calculate the perimeter
        perimeter = rectangle_perimeter(
            length = args.length, # Get the length from the parsed arguments
            width = args.width # Get the width from the parsed arguments
        )

        if perimeter is None:
            return None
        else:
            # Calculate the area
            area = rectangle_area(args.length, args.width)
            
            out_message = (
                "Program ran succesfully!\n"
                f"Length = {args.length}\n"
                f"Width = {args.width}\n"
                f"perimeter = 2 * ({args.length} + {args.width}) = {perimeter}\n"
                f"Area of the rectangle = {args.length} * {args.width} = {area}"
            )

            # Print the results to the console
            logger.info(out_message)
            
            # Save the results to a file if the user provided a filepath
            save_results(out_message, args.out)

    except Exception as e:
        logger.error(e)
        return None


#------------------------------------------------------------#
#---------------- Run the main() function -------------------#
#------------------------------------------------------------#

if __name__ == "__main__":
    main()