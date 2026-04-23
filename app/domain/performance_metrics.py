import pandas as pd
import math
import logging
from app.core.logger import Logger


class Performance_Metrics:
    def __init__(self):
        self.logger = Logger(name="Performance Metrics", level=logging.DEBUG).logger

    def hours_to_minutes(self, hours: float) -> float:
        """
        1.0 = 60
        1.5 = 90
        2.0 = 120
        ...
        """
        minutes = hours * 60
        return minutes
    
    def minutes_to_formated_hours(self, minutes: float) -> str:
        """
        60 = 1:00h
        120 = 2:00h
        160 = 2:40h
        """
        hours = int(minutes // 60)
        remaining_minutes = int(round(minutes % 60))
        if remaining_minutes == 60:
            hours += 1
            remaining_minutes = 0
        return f"{hours}:{remaining_minutes:02d}h"

    def convert_pace_to_readable_pace(self, minutes: float) -> float:
        """
        3.5 = 3:30
        4.0 = 4:00
        4.5 = 4:30
        ...
        """
    
    def calculate_race_effort(self, distance: float, elevation: float) -> float:
        """
        
        """
        self.logger.debug(f"Calculating race effort for distance: {distance} and elevation: {elevation}")
        race_effort = distance + (elevation / 100)
        return race_effort

    def calculate_vertical_rate(self, distance: float, elevation: float) -> float:
        """
        
        """
        self.logger.debug(f"Calculating vertical rate for distance {distance} and elevation: {elevation}")
        vertical_rate = elevation / distance
        return vertical_rate

    def calculate_estimated_pace_on_flat_equivalent(self, total_time: float, race_effort: float) -> float:
        """
        
        """
        self.logger.debug(f"Calculating estimated pace on flat equivalent for race effort {race_effort} with total time {total_time}")
        estimated_pace = total_time / race_effort
        return estimated_pace

    def calculate_race_difficulty_score(self, distance: float, elevation: float, alpha: float = 0.7, c: float = 80, k: float = 0.05) -> float:
        """
        score between 1 - 100
        """
        race_effort = self.calculate_race_effort(distance=distance, elevation=elevation)
        vertical_rate = self.calculate_vertical_rate(distance=distance, elevation=elevation)
        raw_score = race_effort + alpha * vertical_rate
        return 100 / (1 + math.exp(-k * (raw_score - c)))
    
    def calculate_race_category(self, distance: float, elevation: float) -> str:
        """
        
        """
        race_effort = self.calculate_race_effort(distance=distance, elevation=elevation)
        if race_effort < 20:
            return f"{race_effort}K"
        elif race_effort < 50:
            return "20K"
        elif race_effort < 100:
            return "50K"
        elif race_effort < 170:
            return "100K"
        return "100M"

    def generate_category_label(self, distance: float, elevation: float) -> float:
        """
        Flat
        Rolling
        Hilly
        Mountainous
        Extreme Mountain
        """

    def calculate_vertical_per_hour(self, total_hours: float, elevation_gain) -> float:
        """
        elevation_gain / total_hours
        """
        self.logger.debug(f"Calculating total vertical meters per hour with {elevation_gain} total meters in {total_hours} hours")
        vertical_per_hour = elevation_gain / total_hours
        return vertical_per_hour