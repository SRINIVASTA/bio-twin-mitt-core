import time
import random
from datetime import datetime, timezone
from typing import Generator
from src.mitt_core.domain.telemetry import ProcessBatchSnapshot


class PIHistorianSimulator:
    """
    Simulates high-frequency industrial internet of things (IIoT) data streaming
    from a standard OSIsoft PI Historian system managing a bioreactor batch.
    """
    def __init__(self, batch_id: str = "BATCH_2026_X90"):
        self.batch_id = batch_id
        self.step_duration = 0.0
        
        # Define baseline normal operating parameters (The Golden Batch Envelope)
        self.base_temp = 25.0
        self.base_ph = 6.5
        self.base_agitation = 120.0
        self.base_aeration = 250.0

    def stream_live_telemetry(
        self, 
        interval_seconds: float = 1.0, 
        inject_fault: bool = False
    ) -> Generator[ProcessBatchSnapshot, None, None]:
        """
        Generates a continuous sequence of Pydantic-validated process snapshots.
        If inject_fault is active, it introduces sudden process deviations.
        """
        while True:
            self.step_duration += interval_seconds / 3600.0  # Increment duration in hours
            
            # Apply normal stochastic noise to process signals
            temp_noise = random.gauss(0, 0.1)
            ph_noise = random.gauss(0, 0.02)
            agitation_noise = random.gauss(0, 1.5)
            aeration_noise = random.gauss(0, 2.0)
            
            # Simulate a physical anomaly or mechanical degradation
            fault_offset = 0.0
            if inject_fault:
                # Rapid upward deviation mirroring an agitation motor coupling failure
                fault_offset = random.uniform(15.0, 35.0)

            payload = {
                "batch_id": self.batch_id,
                "timestamp": datetime.now(timezone.utc),
                "step_duration_hours": round(self.step_duration, 4),
                "parameters": {
                    "temperature": round(self.base_temp + temp_noise, 2),
                    "ph": round(self.base_ph + ph_noise, 2),
                    "agitation_rpm": round(self.base_agitation + agitation_noise + fault_offset, 2),
                    "aeration_rate": round(self.base_aeration + aeration_noise, 2),
                    "substrate_feed_rate": round(0.50 + random.gauss(0, 0.01), 3)
                }
            }
            
            yield ProcessBatchSnapshot(**payload)
            time.sleep(interval_seconds)


if __name__ == "__main__":
    # Test script execution execution validation
    print("Initializing simulated OSIsoft PI Historian data stream loop...")
    simulator = PIHistorianSimulator()
    
    # Capture 3 sample ticks to verify schema serialization
    stream = simulator.stream_live_telemetry(interval_seconds=0.5, inject_fault=False)
    for _ in range(3):
        snapshot = next(stream)
        print(f"\n[IIO-T TICK] {snapshot.timestamp.isoformat()} | Batch Run: {snapshot.batch_id}")
        print(f" Parameters: {snapshot.parameters}")
