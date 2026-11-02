import numpy as np
import pytest
from src.mitt_core.models.pca_detector import PCABioprocessDetector


def test_pca_detector_training_fit():
    """
    Verifies that the PCA Bioprocess Soft Sensor fits normal operational matrices 
    and establishes non-zero GxP statistical process upper control boundaries.
    """
    # 1. Arrange: Construct a clean, predictable synthetic stable manufacturing baseline
    np.random.seed(101)
    stable_batch_data = np.random.normal(
        loc=[25.0, 6.5, 120.0, 250.0, 0.5],
        scale=[0.05, 0.01, 0.5, 1.0, 0.005],
        size=(50, 5)
    )
    
    detector = PCABioprocessDetector(n_components=2, alpha=0.05)
    
    # 2. Act: Train the monitoring matrices
    detector.fit(stable_batch_data)
    
    # 3. Assert: Verify model parameters conform to mathematical expectations
    assert detector._is_trained is True
    assert detector.t2_ucl > 0.0, "Hotelling T² Upper Control Limit must be a positive non-zero value."
    assert detector.spe_ucl > 0.0, "SPE Upper Control Limit must be a positive non-zero value."


def test_pca_detector_alarm_triggering():
    """
    Ensures that extreme process parameter deviations outside the golden batch envelope
    successfully trip the statistical process control limits (Alarms = True).
    """
    # 1. Arrange: Train our soft-sensor matrix with normal reference baseline data
    np.random.seed(101)
    normal_data = np.random.normal(loc=[25.0, 6.5, 120.0], scale=[0.1, 0.01, 1.0], size=(30, 3))
    detector = PCABioprocessDetector(n_components=2, alpha=0.05)
    detector.fit(normal_data)
    
    # 2. Act: Construct an out-of-bounds anomaly snapshot (e.g., severe agitator motor breakdown)
    critical_anomaly_vector = np.array([[25.1, 6.49, 185.0]])  # Agitation is heavily elevated
    evaluation = detector.transform_and_evaluate(critical_anomaly_vector)
    
    # 3. Assert: Check that alarm thresholds flag the deviation
    assert isinstance(evaluation["t2_alarm"], bool)
    assert isinstance(evaluation["spe_alarm"], bool)
    assert (evaluation["t2_alarm"] is True or evaluation["spe_alarm"] is True), \
        "The multi-variable engine must flag this significant operational vector breach."


def test_pca_unfitted_inference_exception():
    """
    Validates that executing evaluation steps before fitting the structural scaling 
    matrices properly blocks execution with a clean RuntimeException wrapper.
    """
    detector = PCABioprocessDetector(n_components=2)
    unfitted_sample = np.array([[25.0, 6.5, 120.0]])
    
    with pytest.raises(RuntimeError) as exc_info:
        detector.transform_and_evaluate(unfitted_sample)
        
    assert "must be fitted before runtime inference" in str(exc_info.value)
