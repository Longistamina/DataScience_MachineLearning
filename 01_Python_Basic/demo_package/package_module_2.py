from loguru import logger

def multiply(x, y):
    if __name__ == "__main__":
        logger.info("This module is being run directly")
    else:
        logger.info("This module is being imported")
    print(f"{x} * {y} = {x * y}")
    return x * y

def divide(x, y):
    if __name__ == "__main__":
        logger.info("This module is being run directly")
    else:
        logger.info("This module is being imported")
    print(f"{x} / {y} = {x / y}")
    return x / y


if __name__ == "__main__": # These codes will not be executed when being imported from other scripts
    _ = multiply(6, 2)  # Assign to _ to avoid printing output in the console
    # | INFO     | __main__:multiply:3 - This module is being run directly
    # 6 * 2 = 12

    _ = divide(8, 2)
    # | INFO     | __main__:divide:3 - This module is being run directly
    # 8 / 2 = 4.0
