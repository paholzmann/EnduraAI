import pandas as pd
import logging
from app.core.logger import Logger

class PerformanceProjection:
    def __init__(self):
        self.logger = Logger(name="Performance Projection", level=logging.DEBUG).logger
    
    def race_placement_projection(self, distance: float, elevation: float, total_time: float) -> float:
        """
        including: where could i podium and filtering by distance, country, month, race_category, min. Competitors
        Example:
            distance: 10.0 (10km)
            elevation: 500 (500m+)
            total_time: 1.0
            race_effort: 15.0 (15km)
            effort_pace: 4.0 (4:00/km)
            finding races where: Top 1, Top 3, Top 10, Top 25%, Median
            output: Race name, distance, elevation, race_effort, projected_finish_time, projected_placement, percentile, fit score
        """

    def best_race_opportunities(self):
        """
        
        """

    def race_time_projection(self):
        """
        output: 
            projected finish time
            projected percentile
            expected rank band
            best case / likely case / conservative case
        """
    
    def performance_equivalent_projection(self):
        """
        input: 15km effort 60min => 15.0, 1.0
        output:
            12km + 300hm in X
            20km + 800hm in Y
            35km + 1500hm in Z
        """
    
    def effort_based_race_matching(self):
        """
        input:
            wished total_time
            wished placement
            wished distance

        output:
            races that fit to the user
            those races are to easy
            those races are to hard
        """