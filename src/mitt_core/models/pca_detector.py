import numpy as np
from typing import Dict, Any, Tuple
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class PCABioprocessDetector:
    """
    Multi-variable Principal Component Analysis (PCA) anomaly detection engine
    optimized for tracking online pharmaceutical fermentation runs (e.g., IndPenSim).
    Tracks Hotelling's T^2 (latent space variation) and SPE/Q-Residuals (residual error).
    """
    def __init__(self, n_components: int = 3, alpha: float = 0.05):
        self.n_components = n_components
        self.alpha = alpha  # Significance level for control limits (e.g., 0.05 for 95%)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components)
        
        # Upper Control Limits (UCL)
        self.t2_ucl = 0.0
        self.spe_ucl = 0.0
        self._is_trained = False

    def fit(self, X: np.ndarray) -> "PCABioprocessDetector":
        """
        Trains the soft sensor scaling matrices and calculates the GxP-compliant
        statistical upper control limits using historical reference 'Golden Batches'.
        """
        if X.shape[0] <= self.n_components:
            raise ValueError("Row count of training matrix must exceed target n_components.")

        # Scale and fit PCA
        X_scaled = self.scaler.fit_transform(X)
        self.pca.fit(X_scaled)
        
        # Calculate scores and residuals for training data
        X_scores = self.pca.transform(X_scaled)
        X_reconstructed = self.pca.inverse_transform(X_scores)
        residuals = X_scaled - X_reconstructed
        
        # 1. Compute Hotelling's T^2 Control Limit via F-Distribution approximation
        variances = np.var(X_scores, axis=0, ddof=1)
        t2_values = np.sum((X_scores ** 2) / variances, axis=1)
        
        n_samples = X.shape[0]
        p = self.n_components
        from scipy.stats import f
        f_stat = f.ppf(1 - self.alpha, p, n_samples - p)
        self.t2_ucl = (p * (n_samples - 1) / (n_samples - p)) * f_stat

        # 2. Compute SPE (Q) Control Limit via Box's approximate Chi-Square method
        spe_values = np.sum(residuals ** 2, axis=1)
        g = np.var(spe_values, ddof=1) / (2 * np.mean(spe_values))
        h = (2 * (np.mean(spe_values) ** 2)) / np.var(spe_values, ddof=1)
        
        from scipy.stats import chi2
        self.spe_ucl = g * chi2.ppf(1 - self.alpha, df=h)
        
        self._is_trained = True
        return self

    def transform_and_evaluate(self, X_sample: np.ndarray) -> Dict[str, Any]:
        """
        Evaluates a single live multi-variable time-series vector against 
        pre-calculated statistical process limits.
        """
        if not self._is_trained:
            raise RuntimeError("Soft sensor engine must be fitted before runtime inference.")
            
        if X_sample.ndim == 1:
            X_sample = X_sample.reshape(1, -1)

        X_scaled = self.scaler.transform(X_sample)
        X_scores = self.pca.transform(X_scaled)
        X_reconstructed = self.pca.inverse_transform(X_scores)
        residual = X_scaled - X_reconstructed

        # Compute runtime metrics
        variances = np.var(self.pca.transform(self.scaler.transform(self.scaler.inverse_transform(X_scaled))), axis=0, ddof=1)
        # Fallback handle to avoid division by zero on static channels
        variances[variances == 0] = 1e-6 
        
        t2_score = float(np.sum((X_scores[0] ** 2) / variances))
        spe_score = float(np.sum(residual[0] ** 2))

        return {
            "t2_value": t2_score,
            "t2_ucl": self.t2_ucl,
            "t2_alarm": t2_score > self.t2_ucl,
            "spe_value": spe_score,
            "spe_ucl": self.spe_ucl,
            "spe_alarm": spe_score > self.spe_ucl,
            "latent_scores": X_scores[0].tolist()
        }
