'''
This script is created to demonstrate the debugging feature of the Visual Studio Code editor.
'''

#----------------------------------------------------------------------------------------------------------#
#-------------------------------------- Define functional modules -----------------------------------------#
#----------------------------------------------------------------------------------------------------------#

from loguru import logger
from pathlib import Path


def get_input():
    """Prompt the user for rectangle dimensions and return them."""
    length = input("Enter the length of the rectangle: ")
    width = input("Enter the width of the rectangle: ")
    filepath = input("Enter the file path to save the results (or press Enter to skip): ")
    return length, width, filepath


def rectangle_perimeter(length, width):
    """Calculate the perimeter of a rectangle."""
    try:
        assert length > 0 and width > 0, "Length and width must be positive numbers."
    except AssertionError as ae:
        logger.error(ae)
        return None
    else:
        return 2 * (length + width)


def rectangle_area(length, width):
    """Calculate the area of a rectangle."""
    try:
        assert length > 0 and width > 0, "Length and width must be positive numbers."
    except AssertionError as ae:
        logger.error(ae)
        return None
    else:
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



#--------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------- Define main() function ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------#

def main():
    try:
        # Input the rectangle dimensions from the user
        length, width, filepath = get_input()

        # Calculate the perimeter
        perimeter = rectangle_perimeter(
            length = length, # Get the length from the parsed arguments
            width = width # Get the width from the parsed arguments
        )

        # Calculate the area
        area = rectangle_area(length, width)

        if (perimeter is not None) and (area is not None):
            out_message = (
                "\n"
                f"Length = {length}\n"
                f"Width = {width}\n"
                f"perimeter = 2 * ({length} + {width}) = {perimeter}\n"
                f"Area of the rectangle = {length} * {width} = {area}"
            )

            # Print the results to the console
            logger.info(out_message)
            
            # Save the results to a file if the user provided a filepath
            save_results(out_message, filepath)

    except Exception as e:
        logger.error(e)
        return None


#------------------------------------------------------------#
#---------------- Run the main() function -------------------#
#------------------------------------------------------------#

if __name__ == "__main__":
    main()