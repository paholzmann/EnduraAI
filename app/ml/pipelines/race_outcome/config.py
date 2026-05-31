from dataclasses import dataclass, field


@dataclass
class RaceOutcomeConfig:

    data_path: str = (
        "data/processed/utmb/utmb-race-data-features.csv"
    )

    group_column: str = "Race_Title_Cleaned"

    features: list[str] = field(
        default_factory=lambda: [
                "Distance",
                "Elevation_Gain",
                "Elevation_per_km",
                "Race_Effort",
                "Effort_per_km",
                "N_Results"
        ]
    )

    targets: list[str] = field(
        default_factory=lambda: [
            "Winning_Time",
            "Median_Time",
            "Slowest_Time"
        ]
    )

    n_splits: int = 1

    test_size: float = 0.2

    random_state: int = 42

    n_estimators: int = 300

    n_jobs: int = -1

    n_repeats: int = 10

    calculate_permutation_importance: bool = True

    def save_config_data(self) -> dict:
        return {
            "data_path": self.data_path,
            "group_column": self.group_column,
            "features": self.features,
            "targets": self.targets,
            "n_splits": self.n_splits,
            "test_size": self.test_size,
            "random_state": self.random_state,
            "n_estimators": self.n_estimators,
            "n_jobs": self.n_jobs,
            "n_repeats": self.n_repeats
        }