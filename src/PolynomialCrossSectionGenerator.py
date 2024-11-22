import numpy as np

class PolynomialCrossSection:
    def __init__(self):
        self.sigma = np.linspace(0.01, 1, self.N)  # Cross section domain
        # Model parameters
        self.sigma_0 = 0.0                      # Initial cross section
        self.sigma_f = 1.0                      # Final cross section
        self.t_prod = 0.0                       # Production time
        self.t_form = 1.0                       # Formation time

    def calculatePolynomialF_vs_t(self, t, alpha):
        """Polynomial evolution of sigma(t)."""
        sigma_ratio = self.sigma_0 / self.sigma_f
        time_ratio = (t - self.t_prod) / (self.t_form - self.t_prod)
        polynomial_f = self.sigma_f * (1 - sigma_ratio) * (time_ratio ** alpha) + sigma_ratio
        return polynomial_f / self.sigma_f
    
    def calculatePolynomialDsigmaDt_vs_sigma(self, alpha):
        """Polynomial evolution of dsigma/dt."""
        sigma_ratio = self.sigma_0 / self.sigma_f
        polynomial_A = alpha * (self.sigma_f / (self.t_form - self.t_prod)) * (1 - sigma_ratio)
        polynomial_dsigma_dt = polynomial_A * ((self.sigma * self.sigma_f - sigma_ratio + 1e-6)/(1.0 - sigma_ratio)) ** ((alpha - 1.0) / alpha)
        return polynomial_dsigma_dt
    
    def calculatePolynomialDsigmaDt_vs_t(self, t, alpha):
        """Polynomial evolution of dsigma/dt."""
        sigma_ratio = self.sigma_0 / self.sigma_f
        polynomial_A = alpha * (self.sigma_f / (self.t_form - self.t_prod)) * (1 - sigma_ratio)
        polynomial_dsigma_dt = polynomial_A * (t ** (alpha - 1.0))
        return polynomial_dsigma_dt