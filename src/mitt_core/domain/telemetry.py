from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator


class SensorObservation(BaseModel):
    """
    Validates a high-frequency telemetry observation from a single sensor tag.
    """
    tag_name: str = Field(
        ..., 
        description="The unique identifier for the PI Historian sensor tag."
    )
    timestamp: datetime = Field(
        ..., 
        description="The exact UTC timestamp of the measurement."
    )
    value: float = Field(
        ..., 
        description="The numerical value recorded by the sensor."
    )
    status: str = Field(
        default="Good", 
        description="The reliability status of the data point (e.g., Good, Bad, Calibrating)."
    )

    class Config:
        frozen = True
        schema_extra = {
            "example": {
                "tag_name": "IND_PEN_SIM_AGITATION_RPM",
                "timestamp": "2026-11-02T17:00:00Z",
                "value": 120.5,
                "status": "Good"
            }
        }


class ProcessBatchSnapshot(BaseModel):
    """
    Enforces a strict data contract for a multi-variable snapshot of a fermentation batch.
    Maps directly onto the critical process parameters (CPPs) of the IndPenSim process.
    """
    batch_id: str = Field(
        ..., 
        description="Unique identifier for the active fermentation batch run."
    )
    timestamp: datetime = Field(
        ..., 
        description="The operational timestamp for this specific process step."
    )
    step_duration_hours: float = Field(
        ..., 
        ge=0.0, 
        description="The time elapsed since the start of the current batch phase."
    )
    
    # Core Process Parameters (CPPs)
    parameters: Dict[str, float] = Field(
        ..., 
        description="Key process metrics like Aeration, Agitation, Temp, pH, and Feed Rates."
    )
    
    # Optional Spectral Channels (e.g., Offline Raman Spectroscopy)
    raman_spectra: Optional[List[float]] = Field(
        default=None, 
        description="High-dimensional spectral channels used for latent variable soft-sensing."
    )

    @validator("parameters")
    def validate_critical_parameters(cls, v: Dict[str, float]) -> Dict[str, float]:
        """
        Ensures foundational bioprocess parameters are present in the packet.
        """
        required_tags = {"temperature", "ph", "agitation_rpm", "aeration_rate"}
        missing_tags = required_tags - set(v.keys())
        if missing_tags:
            raise ValueError(f"Missing critical telemetry tags: {missing_tags}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "batch_id": "BATCH_2026_101",
                "timestamp": "2026-11-02T17:05:00Z",
                "step_duration_hours": 14.5,
                "parameters": {
                    "temperature": 25.4,
                    "ph": 6.85,
                    "agitation_rpm": 120.0,
                    "aeration_rate": 250.2,
                    "substrate_feed_rate": 0.45
                }
            }
        }
