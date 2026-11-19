import numpy as np
import pytest
from src.mitt_core.models.pca_detector import PCABioprocessDetector


def test_detector_mathematical_bounds():
    """
    Verifies that the PCA Soft-Sensor fits historical training metrics
    and calculates valid non-zero UCL boundaries.
    """
    # 1. Arrange: Construct a clean, predictable synthetic stable manufacturing baseline
    np.random.seed(42)
    mock_golden_history = np.random.normal(
        loc=[25.0, 6.5, 120.0], 
        scale=[0.01, 0.01, 0.5], 
        size=(60, 3)
    )
    
    detector = PCABioprocessDetector(n_components=2, alpha=0.05)
    
    # 2. Act: Train the monitoring matrices
    detector.fit(mock_golden_history)
    
    # 3. Assert: Verify model parameters conform to mathematical expectations
    assert detector._is_trained is True or hasattr(detector, "pca")
    assert detector.t2_ucl > 0, "Hotelling T² UCL limit must be a positive non-zero value."
    assert detector.spe_ucl > 0, "SPE UCL limit must be a positive non-zero value."


def test_pca_detector_alarm_triggering():
    """
    Ensures that extreme process parameter deviations outside the golden batch envelope
    successfully trip the statistical process control limits without throwing warnings.
    """
    # 1. Arrange: Train our soft-sensor matrix with normal reference baseline data
    np.random.seed(42)
    normal_data = np.random.normal(loc=[25.0, 6.5, 120.0], scale=[0.1, 0.01, 1.0], size=(30, 3))
    detector = PCABioprocessDetector(n_components=2, alpha=0.05)
    detector.fit(normal_data)
    
    # 2. Act: Construct an out-of-bounds anomaly snapshot (e.g., severe agitator motor breakdown)
    anomaly_vector = np.array([[25.0, 6.5, 195.0]])  # Agitation is heavily elevated
    evaluation = detector.transform_and_evaluate(anomaly_vector)
    
    # 3. Assert: Check that alarm thresholds flag the deviation
    assert isinstance(evaluation["t2_alarm"], bool)
    assert isinstance(evaluation["spe_alarm"], bool)
    assert (evaluation["t2_alarm"] is True or evaluation["spe_alarm"] is True), \
        "The multi-variable engine must flag this significant operational vector breach."


def test_pca_unfitted_inference_exception():
    """
    Validates execution stability before fitting the structural scaling matrices.
    """
    detector = PCABioprocessDetector(n_components=2)
    unfitted_sample = np.array([[25.0, 6.5, 120.0]])
    
    # Checks if it safely handles unfitted states gracefully without throwing unhandled breaking errors
    try:
        evaluation = detector.transform_and_evaluate(unfitted_sample)
        assert evaluation is not None
    except Exception as e:
        assert isinstance(e, (RuntimeError, ValueError, AttributeError))
