import numpy as np
import pytest
from src.mitt_core.models.pca_detector import PCABioprocessDetector


def test_detector_mathematical_bounds():
    np.random.seed(42)
    mock_golden_history = np.random.normal(loc=[25.0, 6.5, 120.0], scale=[0.01, 0.01, 0.5], size=(60, 3))
    
    detector = PCABioprocessDetector(n_components=2)
    detector.fit(mock_golden_history)
    
    assert detector._is_trained is True
    assert detector.t2_ucl > 0
    assert detector.spe_ucl > 0

    anomaly_vector = np.array([[25.0, 6.5, 195.0]]) # Massive agitation motor surge step
    evaluation = detector.transform_and_evaluate(anomaly_vector)
    
    assert (evaluation["t2_alarm"] is True or evaluation["spe_alarm"] is True)
