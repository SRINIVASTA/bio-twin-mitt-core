import os
import pickle
import numpy as np
from src.mitt_core.models.pca_detector import PCABioprocessDetector
from config.base import GOLDEN_BATCH_TARGETS, GOLDEN_BATCH_SIGMAS, STATISTICAL_CONTROL_LIMITS


class LocalModelTrainer:
    """Manages hyperparameter fits and saves local binary storage states."""
    def __init__(self, output_path: str = "src/ui/components/"):
        self.output_path = output_path

    def run_local_training(self) -> str:
        # Construct synthetic operational history footprint matrix 
        np.random.seed(42)
        training_matrix = np.random.normal(
            loc=list(GOLDEN_BATCH_TARGETS.values()),
            scale=list(GOLDEN_BATCH_SIGMAS.values()),
            size=(250, 5)
        )
        
        detector = PCABioprocessDetector(
            n_components=STATISTICAL_CONTROL_LIMITS["pca_n_components"],
            alpha=STATISTICAL_CONTROL_LIMITS["alpha_significance"]
        )
        detector.fit(training_matrix)
        
        target_file = "pca_calibrated_model.pkl"
        with open(target_file, "wb") as f:
            pickle.dump(detector, f)
        return target_file


if __name__ == "__main__":
    trainer = LocalModelTrainer()
    out = trainer.run_local_training()
    print(f"Model generated successfully: {out}")
