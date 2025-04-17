import datetime as dt
import logging


class ETLLogger:

    def __init__(self, file_name: str):
        """
        A class used to create and configure a logger for forecasting models.

        Attributes:
        today (str): The current date in the format "YYYYMMDD".
        file_name (str): The name of the log file.

        Methods:
        get_logger(self) -> logging.Logger: Returns a logger instance with the specified file name.
        """

        self.today = dt.datetime.now().strftime("%Y%m%d")

        handlers = [logging.StreamHandler()]

        logging.basicConfig(
            format="%(name)s || %(asctime)s || (%(levelname)s) || %(message)s",
            level=logging.INFO,
            handlers=handlers,
        )

        self.file_name = file_name

    def get_logger(self):
        """
        Returns a logger instance with the specified file name.

        Parameters:
        file_name (str): The name of the log file.

        Returns:
        logging.Logger: A logger instance with the specified file name.
        """
        logger = logging.getLogger(self.file_name)
        logger.setLevel("INFO")

        return logger
