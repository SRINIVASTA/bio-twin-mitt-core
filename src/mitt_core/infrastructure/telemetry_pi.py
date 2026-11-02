import time
import random
from datetime import datetime, timezone
from typing import Generator
from src.mitt_core.domain.telemetry import ProcessBatchSnapshot
from config.base import GOLDEN_BATCH_TARGETS, GOLDEN_BATCH_SIGMAS


class PIHistorianSimulator:
    """Emulates live high-frequency plant streaming vectors generated from bioreactor loops."""
    def __init__(self, batch_id: str = "BATCH-2026-MITT"):
        self.batch_id = batch_id
        self.step_duration = 0.0

    def stream_live_telemetry(self, interval_seconds: float = 0.2, inject_fault: bool = False) -> Generator[ProcessBatchSnapshot, None, None]:
        while True:
            self.step_duration += interval_seconds / 3600.0
            
            temp_noise = random.gauss(0, GOLDEN_BATCH_SIGMAS["temperature"])
            ph_noise = random.gauss(0, GOLDEN_BATCH_SIGMAS["ph"])
            agitation_noise = random.gauss(0, GOLDEN_BATCH_SIGMAS["agitation_rpm"])
            aeration_noise = random.gauss(0, GOLDEN_BATCH_SIGMAS["aeration_rate"])
            
            fault_offset = random.uniform(25.0, 45.0) if inject_fault else 0.0

            payload = {
                "batch_id": self.batch_id,
                "timestamp": datetime.now(timezone.utc),
                "step_duration_hours": round(self.step_duration, 4),
                "parameters": {
                    "temperature": round(GOLDEN_BATCH_TARGETS["temperature"] + temp_noise, 2),
                    "ph": round(GOLDEN_BATCH_TARGETS["ph"] + ph_noise, 2),
                    "agitation_rpm": round(GOLDEN_BATCH_TARGETS["agitation_rpm"] + agitation_noise + fault_offset, 2),
                    "aeration_rate": round(GOLDEN_BATCH_TARGETS["aeration_rate"] + aeration_noise, 2),
                    "substrate_feed_rate": round(GOLDEN_BATCH_TARGETS["substrate_feed_rate"] + random.gauss(0, GOLDEN_BATCH_SIGMAS["substrate_feed_rate"]), 3)
                }
            }
            yield ProcessBatchSnapshot(**payload)
            time.sleep(interval_seconds)
