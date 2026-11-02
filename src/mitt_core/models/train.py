import os
import pickle
import pandas as pd
import numpy as np
from src.mitt_core.models.pca_detector import PCABioprocessDetector
from config.base import STATISTICAL_CONTROL_LIMITS, PCA_FEATURE_ORDER


class LocalModelTrainer:
    """
    Orchestrates the loading, cleaning, validation, and training of the
    multivariable PCA soft-sensor engine using localized CSV data files.
    """
    def __init__(self, data_dir: str = "data/processed/", output_dir: str = "src/ui/components/"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def train_from_local_csv(self, filename: str = "indpensim_golden_reference.csv") -> str:
        """
        Ingests a historical bioprocess data sheet, extracts the required features,
        fits the multi-variable statistical control bounds, and serializes the model.
        """
        csv_path = os.path.join(self.data_dir, filename)
        
        # Guard clause: Verify the local data sheet is available
        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Training dataset path not found: '{csv_path}'. "
                "Please run 'python src/mitt_core/infrastructure/local_csv_exporter.py' "
                "to generate the mock reference dataset first."
            )

        print(f"[TRAIN] Loading historical reference dataset from: {csv_path}")
        
        # 1. Read the historical process parameters from disk
        df = pd.read_csv(csv_path)
        
        # 2. Extract and sequence the arrays matching the exact PCA feature layout order
        try:
            X_train = df[PCA_FEATURE_ORDER].dropna().to_numpy()
        except KeyError as e:
            raise KeyError(
                f"Missing expected sensor parameters in CSV dataset columns. "
                f"Required features: {PCA_FEATURE_ORDER}. Error details: {str(e)}"
            )

        if X_train.shape[0] < 10:
            raise ValueError(
                f"Insufficient valid data records found in CSV file. "
                f"Extracted shape: {X_train.shape}. Min rows required: 10."
            )
            
        print(f"[TRAIN] Cleaned training feature matrix generated. Shape: {X_train.shape}")
        
        # 3. Instantiate and calibrate the latent variable statistical detector matrix
        detector = PCABioprocessDetector(
            n_components=STATISTICAL_CONTROL_LIMITS["pca_n_components"],
            alpha=STATISTICAL_CONTROL_LIMITS["alpha_significance"]
        )
        
        print(f"[TRAIN] Calibrating PCA Soft-Sensor (n_components={detector.n_components}, alpha={detector.alpha})...")
        detector.fit(X_train)
        
        # 4. Serialize the calibrated model artifact straight to disk as a binary package
        output_model_file = os.path.join("pca_calibrated_model.pkl")
        with open(output_model_file, "wb") as f:
            pickle.dump(detector, f)
            
        print(f"[✓] Calibrated soft sensor built successfully. Saved model artifact to: {output_model_file}")
        return output_model_file


if __name__ == "__main__":
    trainer = LocalModelTrainer()
    try:
        model_file = trainer.train_from_local_csv()
    except FileNotFoundError as e:
        print(f"[ERROR] {str(e)}")
        print("\n[TIP] Automatically generating the mock tracking data sheet to bypass error...")
        from src.mitt_core.infrastructure.local_csv_exporter import LocalDataProvisioner
        provisioner = LocalDataProvisioner()
        provisioner.generate_golden_batch_csv()
        
        # Re-run training sequence after file initialization complete
        model_file = trainer.train_from_local_csv()
