import os
import numpy as np
import pandas as pd
from GaussianProcessCrossSectionGenerator import GaussianProcessCrossSection

def tabulate_gp_cross_section(GP, out_path):
    n = 200  # Number of samples
    As = np.random.uniform(1, 1, size=n)
    Bs = np.random.rand(n) * As

    # Create lists to store data
    phi_vs_dsigma_dt_data = []
    sigma_vs_phi_and_dsigma_dt_data = []
    time_ratio_vs_sigma_data = []

    # Tabulate GP samples
    for idx, (A, B) in enumerate(zip(As, Bs)):
        GP.calculatePhi(A, B)
        GP.calculateDsigmaDt(A, B)
        GP.calculateF(A, B)
        GP.rescaleTime()
        GP.rescaleDsigmaDt()
        GP.rescalePhi(A, B)
        
        for i in range(GP.N):
            phi_vs_dsigma_dt_data.append([idx, GP.phi[i], GP.dsigma_dt[i]])
            sigma_vs_phi_and_dsigma_dt_data.append([idx, GP.sigma[i], GP.phi[i], GP.dsigma_dt[i]])
            time_ratio_vs_sigma_data.append([idx, GP.time_ratio[i], GP.sigma[i]])

    # Create DataFrames
    df_phi_vs_dsigma_dt = pd.DataFrame(phi_vs_dsigma_dt_data, columns=['index', 'phi', 'dsigma_dt'])
    df_sigma_vs_phi_and_dsigma_dt = pd.DataFrame(sigma_vs_phi_and_dsigma_dt_data, columns=['index', 'sigma', 'phi', 'dsigma_dt'])
    df_time_ratio_vs_sigma = pd.DataFrame(time_ratio_vs_sigma_data, columns=['index', 'time_ratio', 'sigma'])

    # Write DataFrames to text files
    df_phi_vs_dsigma_dt.to_string(os.path.join(out_path, 'phi_vs_dsigma_dt.dat'), index=False, float_format='%10.5f')
    df_sigma_vs_phi_and_dsigma_dt.to_string(os.path.join(out_path, 'sigma_vs_phi_and_dsigma_dt.dat'), index=False, float_format='%10.5f')
    df_time_ratio_vs_sigma.to_string(os.path.join(out_path, 'time_ratio_vs_sigma.dat'), index=False, float_format='%10.5f')

if __name__ == '__main__':
    GP = GaussianProcessCrossSection()
    tabulate_gp_cross_section(GP)
