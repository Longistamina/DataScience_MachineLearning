# conda install -c conda-forge loguru
# pip3 install loguru

'''
The Loguru library in Python is a modern, user-friendly logging library designed to simplify 
and enhance the standard Python logging experience. 
'''

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


#------------------------------------------------------------------------------------------------------#
#---------------------- Save the log information into a .txt file for reviewing -----------------------#
#------------------------------------------------------------------------------------------------------#

# Add file sink while keeping the default console output
logger.add("01_Python_Basic/terminal_logs.txt", 
           rotation="1 MB",  # Rotate when file reaches 1MB
           retention="10 days",  # Keep logs for 10 days
           level="INFO") # Only save the "INFO" level and above

logger.info("This is an info message.")