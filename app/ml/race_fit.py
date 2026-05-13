import pandas as pd
import logging
from app.core.logger import Logger

class RaceFit():
    def __init__(self):
        self.logger = Logger(name="Race Fit", level=logging.DEBUG).logger