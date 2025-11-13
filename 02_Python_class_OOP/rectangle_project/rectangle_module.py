from loguru import logger
from pathlib import Path
from argparse import ArgumentParser, HelpFormatter
import json, re, shutil
from termcolor import colored
import multiprocessing


#-----------------------------------------------------------------------------------------------------------#
#--------------------------------- Define Class and its methods --------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

class RectangleCalculator:
    '''
    This class will takes the length and width of a rectangle as inputs, 
    then return the corresponding perimeter and area as outputs.

    It can also read inputs from multiple JSON files.
    The results can be returned in a specified JSON file.
    The class supports multicore computing.
    '''


    def __init__(self, length=None, width=None):
        '''
        input: the path leading to an input directory containing JSON files, or directly to a specified JSON file
        output: the path leading to on output directory to store the results in JSON files, or directly to a specified JSON file
        length: the length of the rectangle (for inplace calculating)
        width: the width of the rectangle (for inplace calculating)
        cores: the number of CPU cores using for parallel computing
        '''
        self._input = ''
        self._output = ''
        self.length = length
        self.width = width
        self.__length = None
        self.__width = None
        self._cores = 2
        self._single_output_path = None
        self._json_count = 0


    def __validate_output_directory(self): # Internal use only, cannot call out when the module is being imported
        match str(self._output):
            case "":
                pass
            
            case _:
                if (Path(self._output).suffix != ""):
                    self._output = Path(self._output)
                    self._output = self._output.parent / self._output.stem # Create a new path without the suffix
                    output_path = colored(str(self._output), (139, 0, 0), attrs=["bold"])
                    logger.warning(f"You have passed inputs from multiple files, so the ouput path should be a directory, automatically set as {output_path}\n")
                
                else:
                    self._output = Path(self._output)
                
                non_json_count = sum([1 for _ in self._output.rglob("*[!.json]")]) # Ensure the directory contains only json file
                
                if (self._output.is_dir()) and (non_json_count == 0):
                    shutil.rmtree(self._output)
                
                self._output.mkdir(exist_ok=True, parents=True)
        
        return self._output


    def __validate_output_file(self, json_output_file): # Internal use only, cannot call out when the module is being imported
        if str(json_output_file) == "":
            return None
        
        elif (str(self._input) != "") and (Path(self._input).is_dir()):
            
            if self._json_count >= 2:
                json_output_file = Path(self._output).joinpath(json_output_file)

            else:
                json_output_file = Path(self._output)
        
        elif str(self._output) == "":
            return None
        
        else:
            json_output_file = Path(self._output)
        
        
        if json_output_file.suffix == "":
            non_json_count = sum([1 for _ in json_output_file.rglob("*[!.json]")]) # Ensure the directory contains only json file
            
            if (json_output_file.is_dir()) and (non_json_count == 0):
                shutil.rmtree(json_output_file)
                json_output_file.mkdir(exist_ok=True)
            
            else:
                json_output_file.mkdir(exist_ok=True, parents=True)
            
            json_output_file = json_output_file.joinpath("nameless.json")

            output_path = colored(str(json_output_file), (139, 0, 0), attrs=["bold"])
            logger.warning(f"The given output file path is actually a directory, automatically set as {output_path}\n")
        
        elif json_output_file.suffix != ".json":
            json_output_file = json_output_file.parent.joinpath(json_output_file.stem + ".json")

            output_path = colored(str(json_output_file), (139, 0, 0), attrs=["bold"])
            logger.warning(f'The given output file path does not end with ".json", automatically set as {output_path}\n')

        return json_output_file


    @staticmethod
    def __valiate_input_number(*numbers): # Internal use only, cannot call out when the module is being imported
        numeric_pattern = r"^\+?\d+\.?\d*$"
        numbers = list(numbers)
        
        for idx, number in enumerate(numbers):
            if re.match(numeric_pattern, str(number)):
                numbers[idx] = float(number)
            
            else:
                numbers[idx] = None
        
        return numbers


    def __load_rectangle_inputs(self, json_rectangle_file): # Internal use only, cannot call out when the module is being imported
        if len(Path(json_rectangle_file).parts) > 1:
            json_file_path = json_rectangle_file
        
        else:
            json_file_path = self._input.joinpath(json_rectangle_file)
        
        with open(json_file_path, "r") as json_pointer:
            length, width = json.load(json_pointer).values()
            length, width = RectangleCalculator.__valiate_input_number(length, width)
        
        if None in [length, width]:
            json_rectangle_file = colored(json_rectangle_file, "yellow", attrs=['bold'])
            datatype_hint = colored("! They are expected to be POSITIVE NUMBERS (greater than zero)", "red", attrs = ['bold'])
            logger.error(f"CORRUPTED inputs are detected in {json_rectangle_file}{datatype_hint}\n")
        
        return length, width
    

    @property
    def perimeter(self):
        if (None in [self.__length, self.__width]) and ((str(self._input) == "") or (not Path(self._input).is_dir())):
            length, width = RectangleCalculator.__valiate_input_number(self.length, self.width)
        
        else:
            length, width = RectangleCalculator.__valiate_input_number(self.__length, self.__width)
        
        if None in [length, width]:
            self.__perimeter = None
        
        else:
            self.__perimeter = 2 * (length + width) # Name it as "self.__perimeter" to prevent user from changing its value 
       
        return self.__perimeter


    @property
    def area(self):
        if (None in [self.__length, self.__width]) and ((str(self._input) == "") or (not Path(self._input).is_dir())):
            length, width = RectangleCalculator.__valiate_input_number(self.length, self.width)
        
        else:
            length, width = RectangleCalculator.__valiate_input_number(self.__length, self.__width)
        
        if None in [length, width]:
            self.__area = None
        
        else:
            self.__area = length * width # Name it as "self.__area" to prevent user from changing its value
        
        return self.__area

    
    def __save_output_file(self):
        if None not in [self.__length, self.__width]:
            length, width = self.__length, self.__width
        
        else:
            length, width = self.length, self.width
        
        result_dict = {
            "length": length,
            "width": width,
            "perimeter": self.perimeter,
            "area": self.area
        }

        if None in [self.__perimeter, self.__area]:
            return None # Don't save the file if its outputs are corrupted
       
        with open(self._single_output_path, "w") as json_pointer:
            json.dump(result_dict, json_pointer, indent=4)

    
    def _display_saving_single_output_message(self):
        result_path = colored(str(self._single_output_path), (139, 0, 0), attrs=["bold"])
        match str(self._output):
            case "":
                return None
            case _:
                logger.info(f"The result is saved in {result_path}\n")

    
    def summary(self, rectangle_output_name="nameless"):
        rectangle_output_name = colored(str(rectangle_output_name), (139, 0, 0), attrs=["bold"])
        prioritize_message = colored(", prioritize them for calculation.", "yellow", attrs=['bold'])

        if (None in [self.__length, self.__width]) and ((str(self._input) == "") or (not Path(self._input).is_dir())):
            length, width = self.length, self.width
        
        else:
            length, width = self.__length, self.__width
        
        match str(self._output):
            case "":
                perimeter_result = colored(f"++ Perimeter = 2 * ({length} + {width}) = {self.perimeter}", "cyan", attrs=["bold"])
                area_result = colored(f"++ Area = {length} * {width} = {self.area}", "cyan", attrs=["bold"])

                out_message = (
                    f"\n\nResult of the {rectangle_output_name} {colored("rectangle:", "white", attrs=["bold"])}\n"
                    f"++ Length = {length}\n"
                    f"++ Width = {width}\n"
                    f"{perimeter_result}\n"
                    f"{area_result}\n"
                )    

                if (str(self._input) == "") and (None in [self.__perimeter, self.__area]):
                    logger.critical("NO valid inputs were given! They are expected to be POSITIVE NUMBERS (greater than zero)")
                    print()
                    return None
                
                elif (str(self._input) != "") and (None in [self.__perimeter, self.__area]):
                    return None
                
                else:
                    if (str(self._input) != "") and (Path(self._input).exists()) and (None not in [self.length, self.width, self.__length, self.__width]):
                        logger.warning(f"Detected valid inputs in {rectangle_output_name}{prioritize_message}\n")
                                        
                    return out_message # This will make thi message printed out when being imported, avoid showing twice
            
            case _:
                if (str(self._input) != "") and (Path(self._input).exists()) and (None not in [self.length, self.width, self.__length, self.__width]):
                    logger.warning(f"Detected valid inputs in {rectangle_output_name}{prioritize_message}\n")
                
                self.__save_output_file()

                return None


    def _single_workflow(self, json_rectangle_file):
        self.length, self.width = RectangleCalculator.__valiate_input_number(self.length, self.width)
        
        match json_rectangle_file:
            case "":
                if None in [self.length, self.width]: # Check if the given inputs from -l and -w are valid
                    match str(self._input):
                        case "":
                            logger.critical("NO valid inputs were given! They are expected to be POSITIVE NUMBERS (greater than zero)")
                    
                        case _:
                            logger.critical("NO valid inputs were detected by -l (--length) and -w (--width) either!")
                    
                    print()         
                    self._output = "" # To avoid displaying the log "The result is saved in None"     
                    return None
                
                else:
                    self._single_output_path = self.__validate_output_file(self._output)

            case _: # If the input JSON file is given, use its data for calculation
                self.__length, self.__width = self.__load_rectangle_inputs(json_rectangle_file)    

                if Path(self._input).is_dir() and (self._json_count >= 2):  
                    self._single_output_path = self.__validate_output_file(json_rectangle_file)
                    
                elif ((Path(self._input).is_dir()) and (self._json_count == 1)) or (Path(self._input).is_file()):
                    if (None in [self.__length, self.__width]) and (None not in [self.length, self.width]):
                        logger.debug("Detected valid inputs given by -l (--length) and -w (--width), using them for calculation\n")
                        json_rectangle_file = "" # To avoid using the name of corrupted file in the summary()
                    
                    elif (None in [self.__length, self.__width]) and (None in [self.length, self.width]):
                        logger.critical("NO valid inputs were detected by -l (--length) and -w (--width) either!")
                        print()
                        self._output = "" # To avoid displaying the log "The result is saved in None"
                        return None
                
                    self._single_output_path = self.__validate_output_file(self._output)
        
        
        if str(json_rectangle_file).endswith(".json") and Path(self._input).exists() and (str(self._input) != ""):
            out_message = self.summary(Path(json_rectangle_file).name)
        
        else:
            out_message = self.summary()
        
        if out_message is not None:
            logger.info(out_message)
            

#------------------------------------------------------------------------------------------------------------#
#------------------------------------------ Define log_file() function --------------------------------------#
#------------------------------------------------------------------------------------------------------------#

def __config_log_file(project_dir): # Internal use only, cannot call out when the module is being imported
    logger_path = Path(project_dir).joinpath("rectangle_logs.txt")
    if logger_path.exists():
        logger_path.unlink() # Delete the rectangle_logs.txt of the previous run if existed

    logger.add(sink = logger_path, # The path to the .txt file that saves logs
            rotation="1 MB",  # Rotate when file reaches 1MB
            retention="10 days",  # Keep logs for 10 days
            level="WARNING") # Only save the WARNING level and above


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ Define parse_args() function --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def __parse_args():
    formatter = lambda prog: HelpFormatter(prog, width=200, max_help_position=50)

    parser = ArgumentParser(
        prog = "Rectangle Calculator Program",
        description = "Calculate the perimeter and area of a rectangle.",
        add_help = True,
        formatter_class = formatter
    )
    
    parser.add_argument("-l", "--length", required=False, default=None, metavar="\b", help="Length of the rectangle (expected to be a positive number).")
    parser.add_argument("-w", "--width", required=False, default=None, metavar="\b", help="Width of the rectangle (expected to be a positive number).")
    parser.add_argument("-i", "--input", required=False, default="", metavar="\b", help="Input path leading to a JSON file containing the length and width of a rectangle, or to a directory having multiple JSON input files.")
    parser.add_argument("-o", "--output", required=False, default="", metavar="\b", help="Output path leading to a JSON file to store the results, or to a directory to store multiple JSON output files.")
    parser.add_argument("-c", "--cores", required=False, default=2, type=int, metavar="\b", help="The number of CPU cores to be used for parallel computing.")

    return parser.parse_args()


#------------------------------------------------------------------------------------------------------------#
#------------------------------------------ Define main() function ------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

def main():
    try:
        # calculator = RectangleCalculator(
        #     length = '2',
        #     width = "3.5"
        # )
        # calculator._input = "02_Python_class_OOP/rectangle_project/data"
        # calculator._output = ""
        # calculator._cores = 2

        args = __parse_args()

        calculator = RectangleCalculator(
            length = args.length,
            width = args.width
        )
        calculator._input = args.input
        calculator._output = args.output
        calculator._cores = args.cores

        if (calculator._input != "") and (Path(calculator._input).is_dir()):
            calculator._input = Path(calculator._input)
            
            input_json_files = [(entry.name,) for entry in calculator._input.glob("*.json")]
            calculator._json_count = len(input_json_files)
            
            if calculator._json_count > 1:
                calculator._output = calculator._RectangleCalculator__validate_output_directory()

                match str(calculator._output):
                    case "":
                        logger.warning(
                            (   
                                "\nYou are passing multiple input files but no valid ouput directory path was given!!!"
                                "\nIf you procced, all results will be displayed here WITHOUT being saved!!!"
                            )
                        )
                        
                        answer = input(colored("Would you like to proceed? [y/n]: ", "blue", attrs=["bold"]))

                        if answer.lower() == "y":
                            with multiprocessing.Pool(processes=calculator._cores) as pool:
                                pool.starmap(func=calculator._single_workflow, iterable=input_json_files)
                        
                        else:
                            return None # stop the program
                        
                    case _:
                        __config_log_file(calculator._input.parent) # Only produce rectangle_logs.txt if the input and output directories or files are given           
                        
                        with multiprocessing.Pool(processes=calculator._cores) as pool:
                                pool.starmap(func=calculator._single_workflow, iterable=input_json_files)
                        
                        # for entry in calculator._input.glob("*.json"):
                        #     calculator._single_workflow(entry.name)
                        
                        output_dir = colored(str(calculator._output), (139, 0, 0), attrs=["bold"])
                        logger.info(f"All result files are saved in {output_dir}\n")
            
            elif calculator._json_count == 1:
                logger.debug("Only one input JSON file is detected in the given directory. If the output path is also given, it should be in a file format.\n")
                calculator._input = calculator._input.joinpath(input_json_files[0][0])
                calculator._single_workflow(calculator._input)
                calculator._display_saving_single_output_message()
            
            else:
                logger.warning("The given input directory has no JSON file! Use inputs from -l (--length) and -w (--width) for calculation\n")
                calculator._single_workflow('') 
                calculator._display_saving_single_output_message() 

        elif Path(calculator._input).is_file():
            calculator._input = Path(calculator._input)
            
            if Path(calculator._input).suffix == ".json":
                calculator._single_workflow(calculator._input)         

            else:
                logger.warning("The given input path is not a JSON file! Use inputs from -l (--length) and -w (--width) for calculation")
                calculator._single_workflow('')       
            
            calculator._display_saving_single_output_message()

        else:
            if calculator._input != "":
                logger.warning("The given input path does not exist! Use inputs from -l (--length) and -w (--width) for calculation\n")
            
            calculator._single_workflow('')
            calculator._display_saving_single_output_message()

    
    except Exception as e:
        logger.critical(f"{e}\n")


#---------------------------------------------------------------------------------------------------------#
#------------------------------------------ Run main() function ------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    main()
    logger.info("Program ended! Thank you!\n")
