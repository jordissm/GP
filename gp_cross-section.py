import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import matplotlib

matplotlib.use('TkAgg')

# Set formatting options
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": "Computer Modern Roman",
    "text.latex.preamble": r'\usepackage{amsmath}',
    "axes.labelsize": 14,
    "font.size": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

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
    

    
    def plot(self):     
        n = 200  # Number of samples
        t = np.linspace(0, 1, self.N)
        As = np.random.uniform(1, 1, size=n)
        Bs = np.random.rand(n) * As
        
        # Create figures and axes
        fig1, ax1 = plt.subplots(1,1, figsize=(3.04,3.04), dpi=150, sharex=True)
        fig2, ax2 = plt.subplots(2,1, figsize=(3.04,5), dpi=150, sharex=True)
        fig3, ax3 = plt.subplots(1,1, figsize=(3.04,3.04), dpi=150, sharex=True)

        # Set axes limits
        ax1.set_xlim(-6.5, 6.5)
        # ax1.set_ylim(-0.05, 1.05)
        ax2[0].set_xlim(-0.05, 1.05)
        # ax2[0].set_ylim(-0.05, 1.05)
        ax2[1].set_ylim(-0.25, 6.25)
        # ax3.set_xlim(-0.05, 1.05)
        ax3.set_ylim(-0.05, 1.05)

        # Set axes labels
        ax1.set_xlabel(r'${\displaystyle \phi(\sigma)}$')
        ax1.set_ylabel(r'${\displaystyle \frac{d\sigma(t)}{dt}}$')
        ax2[1].set_xlabel(r'${\displaystyle \sigma(t)/\sigma_f}$')
        ax2[0].set_ylabel(r'${\displaystyle \phi(\sigma)}$')
        ax2[1].set_ylabel(r'${\displaystyle \frac{d\sigma(t)}{dt}}$')
        ax3.set_xlabel(r'${\displaystyle (t-t_\text{prod})/(t_\text{form}-t_\text{prod})}$')
        ax3.set_ylabel(r'${\displaystyle \sigma(t)/\sigma_f}$')

        # Set axes ticks
        ax1.tick_params(which='both', direction='in', labelsize=14, bottom=True, top=True, left=True, right=True)
        ax1.yaxis.set_minor_locator(AutoMinorLocator())
        ax2[0].tick_params(which='both', direction='in', labelsize=14, bottom=True, top=True, left=True, right=True)
        ax2[0].yaxis.set_minor_locator(AutoMinorLocator())
        ax2[1].tick_params(which='both', direction='in', labelsize=14, bottom=True, top=True, left=True, right=True)
        ax2[1].xaxis.set_minor_locator(MultipleLocator(0.1))
        ax2[1].yaxis.set_minor_locator(AutoMinorLocator())
        ax3.tick_params(which='both', direction='in', labelsize=14, bottom=True, top=True, left=True, right=True)
        ax3.xaxis.set_minor_locator(MultipleLocator(0.1))
        ax3.yaxis.set_minor_locator(AutoMinorLocator())

        # Plot GP samples
        for A, B in zip(As, Bs):
            self.calculatePhi(A, B)
            self.calculateDsigmaDt(A, B)
            self.calculateF(A, B)
            self.rescaleTime()
            self.rescaleDsigmaDt()
            self.rescalePhi(A, B)
            
            ax1.plot(self.phi, self.dsigma_dt, color='gray', alpha=0.1)
            ax2[0].plot(self.sigma, self.phi, color='gray', alpha=0.1)
            ax2[1].plot(self.sigma, self.dsigma_dt, color='gray', alpha=0.1)
            ax3.plot(self.time_ratio, self.sigma, color='gray', alpha=0.1)
            
        # Plot polynomial parametrizations
        for alpha in [0.5, 1.0, 2.0, 3.0, 1000.0]:
            ax2[1].plot(self.sigma, self.calculatePolynomialDsigmaDt_vs_sigma(alpha), label=r'$\alpha={}$'.format(alpha))
            ax3.plot(t, self.calculatePolynomialF_vs_t(t, alpha), label=r'$\alpha={}$'.format(alpha))

        # Add legends
        ax2[1].legend(fontsize=10, frameon=False, loc='upper right')

        fig1.tight_layout(pad=0.5, w_pad=0.0, h_pad=0.0)
        fig2.tight_layout(pad=0.5, w_pad=0.0, h_pad=0.0)
        fig3.tight_layout(pad=0.5, w_pad=0.0, h_pad=0.0)
        plt.show()




if __name__ == '__main__':
    GP = GaussianProcessCrossSection()
    GP.plot()