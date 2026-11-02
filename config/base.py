from typing import Dict, Any, List

# =============================================================================
# 🧬 BIOPROCESS TELEMETRY & TAG MANAGEMENT CONFIGURATION
# =============================================================================
SENSOR_TAG_REGISTRY: Dict[str, Dict[str, str]] = {
    "temperature": {
        "description": "Bioreactor Internal Vessel Temperature",
        "unit": "°C"
    },
    "ph": {
        "description": "Fermentation Medium Acid-Base Balance",
        "unit": "pH"
    },
    "agitation_rpm": {
        "description": "Impeller Motor Dynamic Shaft Rotation Speed",
        "unit": "RPM"
    },
    "aeration_rate": {
        "description": "Vessel Bottom Sparger Sterile Air Intake Stream",
        "unit": "L/min"
    },
    "substrate_feed_rate": {
        "description": "Carbon Source Nutrient Intake Mass Feed Control",
        "unit": "kg/hr"
    }
}

PCA_FEATURE_ORDER: List[str] = [
    "temperature",
    "ph",
    "agitation_rpm",
    "aeration_rate",
    "substrate_feed_rate"
]

# =============================================================================
# 📊 GOLDEN BATCH STATISTICAL BOUNDARIES
# =============================================================================
GOLDEN_BATCH_TARGETS: Dict[str, float] = {
    "temperature": 25.0,
    "ph": 6.50,
    "agitation_rpm": 120.0,
    "aeration_rate": 250.0,
    "substrate_feed_rate": 0.500
}

GOLDEN_BATCH_SIGMAS: Dict[str, float] = {
    "temperature": 0.10,
    "ph": 0.02,
    "agitation_rpm": 1.50,
    "aeration_rate": 2.00,
    "substrate_feed_rate": 0.010
}

# =============================================================================
# 📈 SOFT SENSOR & AGENT INFERENCE TUNING METRICS
# =============================================================================
STATISTICAL_CONTROL_LIMITS: Dict[str, Any] = {
    "alpha_significance": 0.05,       
    "pca_n_components": 2,            
    "buffer_memory_limit": 40,        
    "sampling_interval_seconds": 0.2  
}

# Active open production model string replacement to clear decommission error
GROQ_MODEL_TARGET: str = "qwen/qwen3.8-27b"
