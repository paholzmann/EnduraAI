import pandas as pd
import logging
from app.core.logger import Logger

class RaceDatabase():
    def __init__(self):
        self.logger = Logger(name="Race Database", level=logging.DEBUG).logger

    def return_database(self):
        """
        
        """
        