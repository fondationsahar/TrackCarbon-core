import pandas as pd
from datetime import datetime
from pathlib import Path
from src.domain.ports.carbon_intensity_repository import BaseCarbonIntensityRepository


class OnDiskCarbonIntensityRepository(BaseCarbonIntensityRepository):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def get(self, timestamp: datetime, zone: str) -> float:
        df = pd.read_csv(self.file_path)
        return round(
            float(
                df.set_index(["zone", "month", "weekday"]).loc[
                    (zone, timestamp.month, timestamp.weekday()),
                    "mean_carbon_intensity",
                ]
            ),
            2,
        )
