import pandas as pd
import math
import logging
from app.core.logger import Logger


class Performance_Metrics:
    def __init__(self):
        self.logger = Logger(name="Performance Metrics", level=logging.DEBUG).logger
    
    def calculate_race_effort(self, distance: float, elevation: float) -> float:
        """
        
        """
        self.logger.debug(f"Calculating race effort for distance: {distance} and elevation: {elevation}")
        race_effort = distance + (elevation / 100)
        return race_effort
    
    def calculate_pace(self, distance: float, total_minutes: float) -> float:
        """

        """
        self.logger.debug(f"Calculating pace for distance: {distance} with total minutes: {total_minutes}")
        pace = total_minutes / distance
        return pace

    def calculate_vertical_rate(self, distance: float, elevation: float) -> float:
        """
        
        """
        self.logger.debug(f"Calculating vertical rate for distance {distance} and elevation: {elevation}")
        vertical_rate = elevation / distance
        return vertical_rate

    def calculate_estimated_pace_on_flat_equivalent(self, total_time: float, race_effort: float) -> float:
        """
        Estimated pace in minutes
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
        vertical_rate = self.calculate_vertical_rate(distance=distance, elevation=elevation)
        if vertical_rate < 15:
            return "Flat"
        elif vertical_rate >= 15 and vertical_rate < 35:
            return "Rolling"
        elif vertical_rate >= 35 and vertical_rate < 55:
            return "Hilly"
        elif vertical_rate >= 55 and vertical_rate < 80:
            return "Mountain"
        elif vertical_rate >= 80:
            return "Extreme Mountain"

    def calculate_vertical_per_hour(self, total_hours: float, elevation_gain: float) -> float:
        """
        elevation_gain / total_hours
        """
        self.logger.debug(f"Calculating total vertical meters per hour with {elevation_gain} total meters in {total_hours} hours")
        vertical_per_hour = elevation_gain / total_hours
        return vertical_per_hour
    
    def calculate_all(self, distance: float, elevation: float, total_minutes: float, alpha: float = 0.7, c: float = 80, k: float = 0.05) -> dict:
        """
        
        """
        race_effort = self.calculate_race_effort(distance=distance, elevation=elevation)
        pace = self.calculate_pace(distance=distance, total_minutes=total_minutes)
        vertical_rate = self.calculate_vertical_rate(distance=distance, elevation=elevation)
        pace_on_flat_equivalent = self.calculate_estimated_pace_on_flat_equivalent(total_time=total_minutes, race_effort=race_effort)
        race_difficulty_score = self.calculate_race_difficulty_score(distance=distance, elevation=elevation, alpha=alpha, c=c, k=k)
        race_category = self.calculate_race_category(distance=distance, elevation=elevation)
        category_label = self.generate_category_label(distance=distance, elevation=elevation)
        return {
            "Race_effort": race_effort,
            "Pace": pace,
            "Vertical_rate": vertical_rate,
            "Pace_on_flat_equivalent": pace_on_flat_equivalent,
            "Race_difficulty_score": race_difficulty_score,
            "Race_category": race_category,
            "Category_label": category_label
        }