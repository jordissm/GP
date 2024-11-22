import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import matplotlib
import os
import sys
import numpy as np
import pandas as pd
from GaussianProcessCrossSectionGenerator import GaussianProcessCrossSection

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

def plot_gp_cross_section(out_path):
    # Load tabulated data
    df_phi_vs_dsigma_dt = pd.read_csv(os.path.join(out_path, 'phi_vs_dsigma_dt.dat'), sep='\s+')
    df_sigma_vs_phi_and_dsigma_dt = pd.read_csv(os.path.join(out_path, 'sigma_vs_phi_and_dsigma_dt.dat'), sep='\s+')
    df_time_ratio_vs_sigma = pd.read_csv(os.path.join(out_path, 'time_ratio_vs_sigma.dat'), sep='\s+')
    
    # Create figures and axes
    fig1, ax1 = plt.subplots(1, 1, figsize=(3.04, 3.04), dpi=150, sharex=True)
    fig2, ax2 = plt.subplots(2, 1, figsize=(3.04, 5), dpi=150, sharex=True)
    fig3, ax3 = plt.subplots(1, 1, figsize=(3.04, 3.04), dpi=150, sharex=True)

    # Set axes limits
    ax1.set_xlim(-6.5, 6.5)
    ax2[1].set_ylim(-0.25, 6.25)
    ax3.set_ylim(-0.05, 1.05)

    # Set axes labels
    ax1.set_xlabel(r'${\displaystyle \phi(\sigma)}$')
    ax1.set_ylabel(r'${\displaystyle \frac{d\sigma(t)}{dt}}$')
    ax2[0].set_ylabel(r'${\displaystyle \phi(\sigma)}$')
    ax2[1].set_ylabel(r'${\displaystyle \frac{d\sigma(t)}{dt}}$')
    ax2[1].set_xlabel(r'${\displaystyle \sigma(t)/\sigma_f}$')
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

    unique_indices = df_phi_vs_dsigma_dt['index'].unique()

    for idx in unique_indices:
        # Filter data for the current index
        df_phi_vs_dsigma_dt_idx = df_phi_vs_dsigma_dt[df_phi_vs_dsigma_dt['index'] == idx]
        df_sigma_vs_phi_and_dsigma_dt_idx = df_sigma_vs_phi_and_dsigma_dt[df_sigma_vs_phi_and_dsigma_dt['index'] == idx]
        df_time_ratio_vs_sigma_idx = df_time_ratio_vs_sigma[df_time_ratio_vs_sigma['index'] == idx]
            
        # Plot data
        ax1.plot(df_phi_vs_dsigma_dt_idx['phi'], df_phi_vs_dsigma_dt_idx['dsigma_dt'], color='gray', alpha=0.1)
        ax2[0].plot(df_sigma_vs_phi_and_dsigma_dt_idx['sigma'], df_sigma_vs_phi_and_dsigma_dt_idx['phi'], color='gray', alpha=0.1)
        ax2[1].plot(df_sigma_vs_phi_and_dsigma_dt_idx['sigma'], df_sigma_vs_phi_and_dsigma_dt_idx['dsigma_dt'], color='gray', alpha=0.1)
        ax3.plot(df_time_ratio_vs_sigma_idx['time_ratio'], df_time_ratio_vs_sigma_idx['sigma'], color='gray', alpha=0.1)
        
        # Plot polynomial parametrizations
        # for alpha in [0.5, 1.0, 2.0, 3.0, 1000.0]:
        #     ax2[1].plot(GP.sigma, GP.calculatePolynomialDsigmaDt_vs_sigma(alpha), label=r'$\alpha={}$'.format(alpha))
        #     ax3.plot(t, GP.calculatePolynomialF_vs_t(t, alpha), label=r'$\alpha={}$'.format(alpha))

        # Add legends
        # ax2[1].legend(fontsize=10, frameon=False, loc='upper right')

    fig1.tight_layout(pad=0.5, w_pad=0.0, h_pad=0.0)
    fig2.tight_layout(pad=0.5, w_pad=0.0, h_pad=0.0)
    fig3.tight_layout(pad=0.5, w_pad=0.0, h_pad=0.0)

    # Save figures
    fig1.savefig(os.path.join(out_path, 'phi_vs_dsigma_dt.pdf'))
    fig2.savefig(os.path.join(out_path, 'sigma_vs_phi_and_dsigma_dt.pdf'))
    fig3.savefig(os.path.join(out_path, 'time_ratio_vs_sigma.pdf'))

    plt.show()

if __name__ == '__main__':
    plot_gp_cross_section(sys.argv[1])
