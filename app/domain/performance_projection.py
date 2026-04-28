import pandas as pd
import numpy as np
import bisect
import logging
from app.core.logger import Logger
from app.core.utils.file_utils import FileUtils
from app.services.utmb.process import ProcessUTMBData
from app.domain.performance_metrics import Performance_Metrics

class PerformanceProjection:
    def __init__(self):
        self.logger = Logger(name="Performance Projection", level=logging.DEBUG).logger
        self.performance_metrics = Performance_Metrics()
    
    def race_placement_projection(self, utmb_df: pd.DataFrame, distance: float, elevation: float, total_time: float) -> float:
        """
        including: where could i podium and filtering by distance, country, month, race_category, min. Competitors
        schritte:
            race effort berechnen
            rennen mit ähnlichem race effort finden
            schauen welche platzierung man theoretisch hat
            rennen zurückgeben mit der best möglichen platzierung
        Example:
            distance: 10.0 (10km)
            elevation: 500 (500m+)
            total_time: 1.0
            race_effort: 15.0 (15km)
            effort_pace: 4.0 (4:00/km)
            finding races where: Top 1, Top 3, Top 10, Top 25%, Median
            output: Race name, distance, elevation, race_effort, projected_finish_time, projected_placement, percentile, fit score
        """
        race_effort = self.performance_metrics.calculate_race_effort(distance=distance, elevation=elevation)
        pace_on_flat_equivalent = self.performance_metrics.calculate_estimated_pace_on_flat_equivalent(total_time=total_time, race_effort=race_effort)
        # pace_on_flat_equivalent = pace_on_flat_equivalent
        fitting_races = self.effort_based_race_matching(utmb_df=utmb_df, distance=distance, elevation=elevation)
        fitting_races["Time_Based_On_Flat_Equivalent"] = fitting_races["Race_Effort"] * pace_on_flat_equivalent
        def calculate_placement(row):
            results = row["Results"]
            if not isinstance(results, list) or len(results) == 0:
                return None
            results = sorted(results)
            time = row["Time_Based_On_Flat_Equivalent"]
            return bisect.bisect_left(results, time) + 1
        
        fitting_races["Possible_Placement"] = fitting_races.apply(calculate_placement, axis=1)
        return fitting_races
        # def calculate_placement(results):
        #     if not isinstance(results, list):
        #         return np.nan
        #     clean_results = [t for t in results if pd.notna(t) and t > 0]
        #     if clean_results:
        #         return np.nan
        #     possible_placement = bisect.bisect_left(clean_results, total_time)
        #     print(possible_placement)
        # fitting_races["Results"].apply(calculate_placement)



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
    
    def effort_based_race_matching(
        self,
        utmb_df: pd.DataFrame,
        distance: float, elevation: float,
        min_effort_ratio: float = 0.85, max_effort_ratio: float = 1.2
        ) -> pd.DataFrame:
        """
        """
        race_effort = self.performance_metrics.calculate_race_effort(distance=distance, elevation=elevation)
        min_effort = race_effort * min_effort_ratio
        max_effort = race_effort * max_effort_ratio
        fitting_races = utmb_df[(utmb_df["Race_Effort"] > min_effort) & (utmb_df["Race_Effort"] < max_effort)]
        return fitting_races

utmb_df = FileUtils().read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-features.csv")
utmb_df = ProcessUTMBData().parse_race_results(utmb_df=utmb_df)
fitting_races = PerformanceProjection().race_placement_projection(utmb_df=utmb_df, distance=85, elevation=3900, total_time=14.5)
print(fitting_races[fitting_races["Race_Title"].str.contains("mozart", case=False)])