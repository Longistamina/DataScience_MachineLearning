'''
logging is a standard Python module that provides a flexible framework for emitting log messages from Python programs. 

Log message is a text-based record of events that occur within a system, application, or service. 
It provides a structured or unstructured way to track what happened, when it happened, and potentially why, 
aiding in debugging, monitoring, and understanding system behavior.

There are 5 standard levels of logging, each with a specific purpose:
1. DEBUG: Detailed information, typically of interest only when diagnosing problems.
2. INFO: Confirmation that things are working as expected.
3. WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (not causing error).
4. ERROR: An indication that due to a more serious problem, the software has not been able to perform some function.
5. CRITICAL: A very serious error, indicating that the program itself may be unable to continue running.
'''

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