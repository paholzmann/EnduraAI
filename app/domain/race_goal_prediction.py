import logging
from app.core.logger import Logger
from app.domain.performance_metrics import Performance_Metrics


class RaceGoalPrediction:
    def __init__(self):
        self.logger = Logger(name="Race Goal Prediction", level=logging.DEBUG).logger
        self.performance_metrics = Performance_Metrics()

    def _hours_to_hms(self, hours: float) -> str:
        total_seconds = int(hours * 3600)
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def predict_goal_time(
        self,
        recent_distance: float,
        recent_elevation: float,
        recent_finish_time: float,
        target_distance: float,
        target_elevation: float,
        adjustment_factor: float = 0.85,
    ) -> dict:
        """
        Predicts realistic (challenging but achievable) finish time for a target race.

        Args:
            recent_distance: Recent race distance in km
            recent_elevation: Recent race elevation gain in m
            recent_finish_time: Recent race finish time in hours
            target_distance: Target race distance in km
            target_elevation: Target race elevation gain in m
            adjustment_factor: Adjustment multiplier (0.85 = 15% slower = conservative)

        Returns:
            dict with predicted_time_hours, predicted_time_str, and pace metrics
        """
        self.logger.debug(
            f"Predicting goal time: recent({recent_distance}km, {recent_elevation}m in {recent_finish_time}h) "
            f"→ target({target_distance}km, {target_elevation}m)"
        )

        recent_race_effort = self.performance_metrics.calculate_race_effort(
            distance=recent_distance, elevation=recent_elevation
        )
        self.logger.debug(f"Recent race effort: {recent_race_effort}")

        recent_pace_on_flat = self.performance_metrics.calculate_estimated_pace_on_flat_equivalent(
            total_time=recent_finish_time, race_effort=recent_race_effort
        )
        self.logger.debug(f"Recent pace on flat equivalent: {recent_pace_on_flat} hours/effort")

        adjusted_pace_on_flat = recent_pace_on_flat * adjustment_factor
        self.logger.debug(f"Adjusted pace on flat equivalent (×{adjustment_factor}): {adjusted_pace_on_flat} hours/effort")

        target_race_effort = self.performance_metrics.calculate_race_effort(
            distance=target_distance, elevation=target_elevation
        )
        self.logger.debug(f"Target race effort: {target_race_effort}")

        predicted_time_hours = target_race_effort * adjusted_pace_on_flat
        self.logger.debug(f"Predicted finish time: {predicted_time_hours} hours")

        predicted_time_str = self._hours_to_hms(predicted_time_hours)

        return {
            "predicted_time_hours": round(predicted_time_hours, 2),
            "predicted_time_str": predicted_time_str,
            "recent_pace_on_flat": round(recent_pace_on_flat, 4),
            "adjusted_pace_on_flat": round(adjusted_pace_on_flat, 4),
        }
