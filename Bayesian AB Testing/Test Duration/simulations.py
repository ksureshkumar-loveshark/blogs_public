import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import beta
import matplotlib.pyplot as plt
import json
import decimal
decimal.getcontext().prec = 4


def calculate_expected_loss(control_simulation, treatment_simulation, treatment_won, min_difference_delta=0):
    loss_control = [max((j - min_difference_delta) - i, 0) for i,j in zip(control_simulation, treatment_simulation)]
    loss_treatment = [max(i - (j - min_difference_delta), 0) for i,j in zip(control_simulation, treatment_simulation)]

    all_loss_control = [int(i)*j for i,j in zip(treatment_won, loss_control)]
    all_loss_treatment = [(1 - int(i))*j for i,j in zip(treatment_won, loss_treatment)]

    expected_loss_control = np.mean(all_loss_control)
    expected_loss_treatment = np.mean(all_loss_treatment)
    return expected_loss_control, expected_loss_treatment


def run_multiple_experiment_simulations(n, prior_alpha, prior_beta, control_cr, treatment_cr, epsilon, variant_sample_size=10000, min_simulations_per_experiment=0):
    output = pd.DataFrame()

    for simulation in range(0,n):
        records = []
        control_simulations = np.random.binomial(n=1, p=control_cr, size=variant_sample_size)
        treatment_simulations = np.random.binomial(n=1, p=treatment_cr, size=variant_sample_size)
        
        sample_size = 0
        control_conversions = 0
        treatment_conversions = 0

        for i in range(variant_sample_size):
            sample_size += 1
            control_conversions += control_simulations[i]
            treatment_conversions += treatment_simulations[i]

            control_pdfs = np.random.beta(prior_alpha + control_conversions, prior_beta + sample_size - control_conversions, size=1000)
            treatment_pdfs = np.random.beta(prior_alpha + treatment_conversions, prior_beta + sample_size - treatment_conversions, size=1000)
            treatment_pdf_higher = [i <= j for i,j in zip(control_pdfs, treatment_pdfs)]

            expected_loss_control, expected_loss_treatment = calculate_expected_loss(control_pdfs, treatment_pdfs, treatment_pdf_higher)

            if (simulation >= min_simulations_per_experiment) and (expected_loss_treatment <= epsilon):
                records.append({'simulation': simulation+1, 'sample': sample_size, 'treatment_cr': (treatment_conversions/sample_size), 'control_cr': (control_conversions/sample_size), 'treatment_expected_loss': expected_loss_treatment, 'control_expected_loss': expected_loss_control, 'winner': 'treatment'})
            elif (simulation >= min_simulations_per_experiment) and expected_loss_control <= epsilon:
                records.append({'simulation': simulation+1, 'sample': sample_size, 'treatment_cr': (treatment_conversions/sample_size), 'control_cr': (control_conversions/sample_size), 'treatment_expected_loss': expected_loss_treatment, 'control_expected_loss': expected_loss_control, 'winner': 'control'})
            else:
                records.append({'simulation': simulation+1, 'sample': sample_size, 'treatment_cr': (treatment_conversions/sample_size), 'control_cr': (control_conversions/sample_size), 'treatment_expected_loss': expected_loss_treatment, 'control_expected_loss': expected_loss_control, 'winner': 'inconclusive'})

        simulation_results = pd.DataFrame.from_records(records)
        output = pd.concat([output, simulation_results])    
    
    return output


if __name__ == "__main__":

    standard_simulations = run_multiple_experiment_simulations(100, 7, 15, 0.32, 0.32*(1.15), 0.0015)
    standard_simulations.to_csv('experiment_simulations_37.csv', index=False)

    low_mde_simulations = run_multiple_experiment_simulations(100, 7, 15, 0.32, 0.32*(1.05), 0.0015)
    low_mde_simulations.to_csv('experiment_simulations_34.csv', index=False)

    high_mde_simulations = run_multiple_experiment_simulations(100, 7, 15, 0.32, 0.32*(1.3), 0.0015)
    high_mde_simulations.to_csv('experiment_simulations_41.csv', index=False)

    low_eps_simulations = run_multiple_experiment_simulations(100, 7, 15, 0.32, 0.32*(1.15), 0.0005)
    low_eps_simulations.to_csv('experiment_simulations_low_eps.csv', index=False)

    high_eps_simulations = run_multiple_experiment_simulations(100, 7, 15, 0.32, 0.32*(1.15), 0.003)
    high_eps_simulations.to_csv('experiment_simulations_high_eps.csv', index=False)

    low_lambda_simulations = run_multiple_experiment_simulations(100, 2, 20, 0.05, 0.05*(1.15), 0.05*(0.005))
    low_lambda_simulations.to_csv('experiment_simulations_low_lambda.csv', index=False)

    high_lambda_simulations = run_multiple_experiment_simulations(100, 13, 9, 0.6, 0.6*(1.15), 0.6*(0.005))
    high_lambda_simulations.to_csv('experiment_simulations_high_lambda.csv', index=False)

    

