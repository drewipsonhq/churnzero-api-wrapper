import logging

COLORS = {
    "RESET": "\033[0m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "ORANGE": "\033[38;5;208m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
}


class ColoredFormatter(logging.Formatter):

    def format(self, record):
        """
        Add color codes to the log level name
        """
        level_color = {
            logging.DEBUG: COLORS["CYAN"],
            logging.INFO: COLORS["GREEN"],
            logging.WARNING: COLORS["ORANGE"],
            logging.ERROR: COLORS["RED"],
            logging.CRITICAL: COLORS["RED"],
        }.get(record.levelno, COLORS["RESET"])

        # Add color codes only to the level name
        record.levelname = level_color + record.levelname + COLORS["RESET"]

        # Call the original formatter to format the rest of the message
        message = super().format(record)

        return message


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter("%(levelname)s:%(message)s"))
    logger.addHandler(handler)

    return logger
