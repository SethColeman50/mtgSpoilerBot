import logging
import sys

def main():
    from bot.bot import start_bot
    start_bot()

def get_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    logging.basicConfig(filename=filename, level=logging.INFO)

    return logger

if __name__ == "__main__":
    main()