import numpy as np
from loguru import logger


def main():
    lucky_number = "".join(np.random.randint(0, 10, 8).astype(str).tolist())

    lucky_number = f"Your lucky number is: {lucky_number}"

    message = (
        "\n" + "="*len(lucky_number)
        + f"\n{lucky_number}\n"
        + "="*len(lucky_number)
    )

    logger.info(message)

if __name__ == "__main__":
    main()
