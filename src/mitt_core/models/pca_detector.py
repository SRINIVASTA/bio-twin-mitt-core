import numpy as np
from typing import Dict, Any
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import f, chi2


class PCABioprocessDetector:
    """Calculates online multi-variable tracking indices (Hotelling's T^2 & SPE Control Limits)."""
    def __init__(self, n_components: int = 2, alpha: float = 0.05):
        self.n_components = n_components
        self.alpha = alpha
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components)
        self.t2_ucl = 0.0
        self.spe_ucl = 0.0
        self.training_scores_var = None  # Freezes baseline variance matrix shapes
        self._is_trained = False

    def fit(self, X: np.ndarray) -> "PCABioprocessDetector":
        X_scaled = self.scaler.fit_transform(X)
        self.pca.fit(X_scaled)
        
        X_scores = self.pca.transform(X_scaled)
        X_reconstructed = self.pca.inverse_transform(X_scores)
        residuals = X_scaled - X_reconstructed
        
        # Calculate and cache baseline training scores variance safely
        self.training_scores_var = np.var(X_scores, axis=0, ddof=1)
        self.training_scores_var[self.training_scores_var == 0] = 1e-6
        
        n_samples = X.shape[0]
        p = self.n_components
        f_stat = f.ppf(1 - self.alpha, p, n_samples - p)
        self.t2_ucl = (p * (n_samples - 1) / (n_samples - p)) * f_stat

        spe_values = np.sum(residuals ** 2, axis=1)
        g = np.var(spe_values, ddof=1) / (2 * np.mean(spe_values))
        h = (2 * (np.mean(spe_values) ** 2)) / np.var(spe_values, ddof=1)
        self.spe_ucl = g * chi2.ppf(1 - self.alpha, df=h)
        
        self._is_trained = True
        return self

    def transform_and_evaluate(self, X_sample: np.ndarray) -> Dict[str, Any]:
        if not self._is_trained:
            raise RuntimeError("Soft sensor model engine must be fitted before runtime inference.")
        if X_sample.ndim == 1:
            X_sample = X_sample.reshape(1, -1)

        X_scaled = self.scaler.transform(X_sample)
        X_scores = self.pca.transform(X_scaled)
        X_reconstructed = self.pca.inverse_transform(X_scores)
        residual = X_scaled - X_reconstructed

        # Use cached baseline variance to avoid Degrees of Freedom divide-by-zero warnings
        t2_score = float(np.sum((X_scores ** 2) / self.training_scores_var))
        spe_score = float(np.sum(residual ** 2))

        return {
            "t2_value": t2_score, "t2_ucl": self.t2_ucl, "t2_alarm": t2_score > self.t2_ucl,
            "spe_value": spe_score, "spe_ucl": self.spe_ucl, "spe_alarm": spe_score > self.spe_ucl,
            "latent_scores": X_scores.tolist()
        }
