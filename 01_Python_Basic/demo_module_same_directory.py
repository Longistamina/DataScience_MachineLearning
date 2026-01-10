from loguru import logger

def add(x, y):
    if __name__ == "__main__":
        logger.info("This module is being run directly")
    else:
        logger.info("This module is being imported")
    print(f"{x} + {y} = {x + y}")
    return x + y

def subtract(x, y):
    if __name__ == "__main__":
        logger.info("This module is being run directly")
    else:
        logger.info("This module is being imported")
    print(f"{x} - {y} = {x - y}")
    return x - y

_ = add(4, 5) # This code will be run when the script is imported for the first time
              # even if the main function does not call it out

if __name__ == "__main__": # These codes will not be executed when being imported from other scripts
    _ = add(5, 3) # Assign to _ to avoid printing output in the console
    # | INFO     | __main__:add:3 - This module is being run directly
    # 5 + 3 = 8

    _ = subtract(10, 4)
    # | INFO     | __main__:subtract:3 - This module is being run directly
    # 10 - 4 = 6