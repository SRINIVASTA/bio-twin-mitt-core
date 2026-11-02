import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from config.base import GOLDEN_BATCH_TARGETS, GOLDEN_BATCH_SIGMAS, PCA_FEATURE_ORDER

class LocalDataProvisioner:
    """
    Generates and exports realistic offline time-series datasets matching 
    the IndPenSim benchmark schema to enable local model training loops.
    """
    def __init__(self, output_dir: str = "data/processed/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_golden_batch_csv(self, filename: str = "indpensim_golden_reference.csv", row_count: int = 500) -> str:
        """
        Creates a time-series spreadsheet of standard, stable bioreactor runs 
        representing optimal manufacturing envelopes (Golden Batches).
        """
        np.random.seed(42)
        base_time = datetime.now() - timedelta(days=5)
        
        # Build systematic timestamps
        timestamps = [base_time + timedelta(minutes=2 * i) for i in range(row_count)]
        
        # Generate stable, normally distributed process matrices
        data_matrix = np.random.normal(
            loc=list(GOLDEN_BATCH_TARGETS.values()),
            scale=list(GOLDEN_BATCH_SIGMAS.values()),
            size=(row_count, len(PCA_FEATURE_ORDER))
        )
        
        # Structure into a clean pandas data frame layer
        df = pd.DataFrame(data_matrix, columns=PCA_FEATURE_ORDER)
        df.insert(0, "timestamp", timestamps)
        df.insert(0, "batch_id", "BATCH-2026-REF-GOLDEN")
        
        # Clean up floating point decimal precision for clean CSV reading
        for col in PCA_FEATURE_ORDER:
            df[col] = df[col].round(4)
            
        output_file_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_file_path, index=False)
        print(f"[✓] Local mock benchmark data generated successfully at: {output_file_path}")
        return output_file_path

if __name__ == "__main__":
    provisioner = LocalDataProvisioner()
    provisioner.generate_golden_batch_csv()
