from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator


class SensorObservation(BaseModel):
    """Validates high-frequency telemetry observation from single sensor tag."""
    tag_name: str = Field(..., description="The unique identifier for sensor tag.")
    timestamp: datetime = Field(..., description="The exact UTC timestamp of measurement.")
    value: float = Field(..., description="The numerical value recorded by the sensor.")
    status: str = Field(default="Good", description="The reliability status of the data point.")

    class Config:
        frozen = True


class ProcessBatchSnapshot(BaseModel):
    """Enforces data contract for multi-variable snapshot of a fermentation batch."""
    batch_id: str = Field(..., description="Unique identifier for the active fermentation run.")
    timestamp: datetime = Field(..., description="The operational timestamp for this step.")
    step_duration_hours: float = Field(..., ge=0.0, description="Elapsed hours since phase start.")
    parameters: Dict[str, float] = Field(..., description="Key process metrics dict.")
    raman_spectra: Optional[List[float]] = Field(default=None, description="High-dimensional spectral channels.")

    @validator("parameters")
    def validate_critical_parameters(cls, v: Dict[str, float]) -> Dict[str, float]:
        required_tags = {"temperature", "ph", "agitation_rpm", "aeration_rate"}
        missing_tags = required_tags - set(v.keys())
        if missing_tags:
            raise ValueError(f"Missing critical telemetry tags: {missing_tags}")
        return v
