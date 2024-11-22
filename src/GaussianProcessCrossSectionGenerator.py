import numpy as np

class GaussianProcessCrossSection:
    def __init__(self):
        """Initialize Gaussian Process Cross-section with default parameters."""
        # Model hyperparameters
        self.N = 100                           # Number of points in the domain
        self.sigma = np.linspace(0.01, 1, self.N)  # Cross section domain
        self.l = 1.0                            # Correlation length (~10% of the domain)
        self.kappa = 10.0                      # Amplitude
        self.xi = 1e-6                          # Small noise term
        # Model parameters
        self.sigma_0 = 0.0                      # Initial cross section
        self.sigma_f = 1.0                      # Final cross section
        self.t_prod = 0.0                       # Production time
        self.t_form = 1.0                       # Formation time
        
        # Compute covariance matrix and Cholesky decomposition
        self.SigmaMatrix = self.calculateCovarianceSigma()
        self.LMatrix = self.calculateCholeskyL()

    def calculateCovarianceSigma(self):
        """Calculate the covariance matrix for the cross-section."""
        # Create a matrix with pairwise differences and apply the function element-wise
        sigma_i = self.sigma[:, np.newaxis]
        sigma_j = self.sigma[np.newaxis, :]
        return self.kappa ** 2 * np.exp(-0.5 * ((sigma_i - sigma_j) / self.l) ** 2)

    def calculateCholeskyL(self):
        """Perform Cholesky decomposition on the covariance matrix."""
        noiseMatrix = self.xi * np.eye(self.N)
        return np.linalg.cholesky(self.SigmaMatrix + noiseMatrix)

    def calculatePhi(self, A, B):
        """Generate the GP sample for phi."""
        mu = 0*np.log((A / self.sigma) - B)
        random_noise = np.dot(self.LMatrix, np.random.normal(size=self.N))
        self.phi = mu + random_noise
        return self.phi

    def calculateDsigmaDt(self, A, B):
        """Compute dsigma/dt based on phi."""
        # Invert auxiliary variable phi to get dsigma/dt
        # phi = ln( (A / dsigma/dt) - B)
        return A / (np.exp(self.phi) + B)
    
    def calculateF(self, A, B):
        """Compute time and cross-section evolution."""
        self.dsigma_dt = self.calculateDsigmaDt(A, B)
        # Integrate dsigma / (dsigma/dt) to get times
        t = np.zeros(self.N)
        for i in range(1, self.N):
            Dsigma = self.sigma[i] - self.sigma[i - 1]
            t[i] = t[i - 1] + (Dsigma / self.dsigma_dt[i])
        self.time_ratio = (t - self.t_prod) / (self.t_form - self.t_prod)
    
    def rescaleTime(self):
        time_ratio_min = np.nanmin(self.time_ratio)
        time_ratio_max = np.nanmax(self.time_ratio)
        numerator = self.time_ratio - time_ratio_min
        denominator = time_ratio_max - time_ratio_min
        self.time_ratio = numerator / denominator

    def rescaleDsigmaDt(self):
        for i in range(1, self.N):
            numerator = self.sigma[i] - self.sigma[i - 1]
            denominator = self.time_ratio[i] - self.time_ratio[i - 1]
            self.dsigma_dt[i] = numerator / denominator
        self.dsigma_dt = np.array(self.dsigma_dt)
    
    def rescalePhi(self, A, B):
        self.phi = np.log((A / self.sigma) - B)