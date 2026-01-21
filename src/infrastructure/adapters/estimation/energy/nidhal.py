from src.domain.models.energy_estimators import SupportedEnergyConsumptionMethod
from src.domain.ports.energy_estimator import BaseEnergyEstimator
from src.domain.models.event import Event

CONSTANT_LATENCY = 0.5


class NidhalEnergyEstimator(BaseEnergyEstimator):
    def __init__(
        self,
        num_gpu_for_inference: int,
        batch_size_used_for_inference: int,
        share_of_total_gpu_power_used: float,
        share_of_total_gpu_power_used_by_non_gpu: float,
        max_rated_power_per_gpu: int,
        max_rated_power_for_non_gpu_parts: int,
        tokens_per_second: int,
        data_center_power_usage_effectiveness: float,
        latency: float,
    ):
        self.num_gpu_for_inference = num_gpu_for_inference
        self.batch_size_used_for_inference = batch_size_used_for_inference
        self.share_of_total_gpu_power_used = share_of_total_gpu_power_used
        self.share_of_total_gpu_power_used_by_non_gpu = (
            share_of_total_gpu_power_used_by_non_gpu
        )
        self.max_rated_power_per_gpu = max_rated_power_per_gpu
        self.max_rated_power_for_non_gpu_parts = max_rated_power_for_non_gpu_parts
        self.tokens_per_second = tokens_per_second
        self.data_center_power_usage_effectiveness = (
            data_center_power_usage_effectiveness
        )
        self.latency = latency

    def compute(self, events: list[Event]) -> float:
        # NOTE: Implicit that it's an AI Event / typing is not very strict here.
        return (
            sum(
                (
                    (
                        (
                            event.event_metadata.num_response_tokens
                            / self.tokens_per_second
                        )
                        + self.latency
                    )
                    / 3600
                )
                * (
                    (
                        self.max_rated_power_per_gpu
                        * self.num_gpu_for_inference
                        * self.share_of_total_gpu_power_used
                        / self.batch_size_used_for_inference
                    )
                    + (
                        self.max_rated_power_for_non_gpu_parts
                        * self.share_of_total_gpu_power_used_by_non_gpu
                        / self.batch_size_used_for_inference
                    )
                )
                * self.data_center_power_usage_effectiveness
                for event in events
            )
            * 1000
        )  # Convert to kWh from Wh

    @property
    def method(self) -> SupportedEnergyConsumptionMethod:
        return SupportedEnergyConsumptionMethod.NIDHAL
