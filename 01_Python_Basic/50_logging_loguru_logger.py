# conda install -c conda-forge loguru
# pip3 install loguru

'''
Log message is a text-based record of events that occur within a system, application, or service. 
It provides a structured or unstructured way to track what happened, when it happened, and potentially why, 
aiding in debugging, monitoring, and understanding system behavior.
logging is a standard Python module that provides a flexible framework 
for emitting log messages from Python programs.

The Loguru library in Python is a modern, user-friendly logging library designed to simplify 
and enhance the standard Python logging experience. 

There are 5 standard levels of logging, each with a specific purpose:
1. DEBUG: Detailed information, typically of interest only when diagnosing problems.
2. INFO: Confirmation that things are working as expected.
3. WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (not causing error).
4. ERROR: An indication that due to a more serious problem, the software has not been able to perform some function.
5. CRITICAL: A very serious error, indicating that the program itself may be unable to continue running.

###############################

Flow of contents:

1. logging
   + Run with default logging level
   + Run with DEBUG logging level
   + Run with INFO logging level
   + Run with WARNING logging level
   + Run with ERROR logging level
   + Run with CRITICAL logging level

2. loguru.logger (from loguru import logger)
   + loguru.logger
   + Save the log information into a .txt file for reviewing
'''

#---------------------------------------------------------------------------------------------#
#------------------------------------ 1. logging ---------------------------------------------#
#---------------------------------------------------------------------------------------------#

import logging

logger = logging.getLogger(__name__) # Get a logger for the current module
                                     # This allows for module-specific logging configuration, 
                                     # and avoids conflicts with other modules.
                                    
def logging_with_level(log_level=None):
    if log_level is not None:
        logging.basicConfig(level=log_level) # Set the logging level to the specified log_level
        logger.setLevel(log_level) # Set the logger's level to the specified log_level
    else:
        logging.basicConfig(level=logging.WARNING) # Set the default logging level to WARNING
        logger.setLevel(logging.WARNING) # Set the logger's level to WARNING               
    
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")


####################################
## Run with default logging level ##
####################################

logging_with_level()
# WARNING:__main__:This is a warning message.
# ERROR:__main__:This is an error message.
# CRITICAL:__main__:This is a critical message.


##################################
## Run with DEBUG logging level ##
##################################

logging_with_level(logging.DEBUG)
# DEBUG:__main__:This is a debug message.
# INFO:__main__:This is an info message.
# WARNING:__main__:This is a warning message.
# ERROR:__main__:This is an error message.
# CRITICAL:__main__:This is a critical message.


#################################
## Run with INFO logging level ##
#################################

logging_with_level(logging.INFO)
# INFO:__main__:This is an info message.
# WARNING:__main__:This is a warning message.
# ERROR:__main__:This is an error message.
# CRITICAL:__main__:This is a critical message.


####################################
## Run with WARNING logging level ##
####################################

logging_with_level(logging.WARNING)
# WARNING:__main__:This is a warning message.
# ERROR:__main__:This is an error message.
# CRITICAL:__main__:This is a critical message.


##################################
## Run with ERROR logging level ##
##################################

logging_with_level(logging.ERROR)
# ERROR:__main__:This is an error message.
# CRITICAL:__main__:This is a critical message.


#####################################
## Run with CRITICAL logging level ##
#####################################

logging_with_level(logging.CRITICAL)
# CRITICAL:__main__:This is a critical message.

'''
logging also allows configuring the output format of log messages,
which can include the timestamp, log level, and message.

However, we will use the loguru library for logging tasks.
This the logging of loguru is already configured and ready to use.
'''


#---------------------------------------------------------------------------------------------#
#--------------------- 2. loguru.logger (from loguru import logger) --------------------------#
#---------------------------------------------------------------------------------------------#

###################
## loguru.logger ##
###################

from loguru import logger

logger.debug("This is a debug message.")
# 2025-07-30 17:34:16.453 | DEBUG    | __main__:<module>:1 - This is a debug message.


logger.info("This is an info message.")
# 2025-07-30 17:34:16.453 | INFO     | __main__:<module>:1 - This is an info message.


logger.warning("This is a warning message.")
# 2025-07-30 17:34:16.454 | WARNING  | __main__:<module>:1 - This is a warning message.


logger.error("This is an error message.")
# 2025-07-30 17:34:16.454 | ERROR    | __main__:<module>:1 - This is an error message.


logger.critical("This is a critical message.")
# 2025-07-30 17:34:16.454 | CRITICAL | __main__:<module>:1 - This is a critical message.

#############################################################
## Save the log information into a .txt file for reviewing ##
#############################################################

# Add file sink while keeping the default console output
logger.add("01_Python_Basic/terminal_logs.txt", 
           rotation="1 MB",  # Rotate when file reaches 1MB
           retention="10 days",  # Keep logs for 10 days
           level="INFO") # Only save the "INFO" level and above

logger.info("This is an info message.")