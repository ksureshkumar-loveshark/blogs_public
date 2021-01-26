import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_peeking_example():
    simulations = pd.read_csv('experiment_simulations_same_cr.csv')
    simulations['sample'] = simulations['sample'] + 1

    for i in set(simulations['simulation'].values):
        if i != 3:
            continue

        filtered_simulation = simulations[simulations['simulation'] == i]

        _, (ax1, ax2) = plt.subplots(1, 2)

        
        ax1.plot(filtered_simulation['sample'], filtered_simulation['treatment_expected_loss'], label='treatment')
        ax1.plot(filtered_simulation['sample'], filtered_simulation['control_expected_loss'], label='control')
        ax1.plot(filtered_simulation['sample'], np.full((10000,), 0.003), label='threshold', linestyle='dashed')
        ax1.set_xlabel('Sample Size')
        ax1.set_ylabel('Expected Loss')
        ax1.set_title('Expected Loss Simulation')
        ax1.legend()
        
        
        ax2.plot(filtered_simulation['sample'], filtered_simulation['treatment_cr'], label='treatment')
        ax2.plot(filtered_simulation['sample'], filtered_simulation['control_cr'], label='control')
        ax2.set_xlabel('Sample Size')
        ax2.set_ylabel('Conversion Rates')
        ax2.set_title('Conversion Rates Simulation')
        ax2.legend()
        # plt.savefig(f'Expected Loss Simulation {i}')
        plt.show()

def plot_simulations(file_name):
    simulations = pd.read_csv(file_name)
    no_of_simulations = simulations['simulation'].max()

    _, (ax1, ax2) = plt.subplots(1, 2)

    for i in range(1, no_of_simulations+1):

        filtered = simulations[simulations['simulation'] == i]


        if i == 1:
            control = ax1.plot(filtered['sample'], filtered['control_expected_loss'], label='control')
            treatment = ax1.plot(filtered['sample'], filtered['treatment_expected_loss'], label='treatment')
            threshold = ax1.plot(filtered['sample'], np.full((10000,), 0.0015), label='threshold', linestyle='dashed')

            ax2.plot(filtered['sample'], filtered['control_cr'], label='control', color=control[0].get_color())
            ax2.plot(filtered['sample'], filtered['treatment_cr'], label='treatment', color=treatment[0].get_color())
        else:
            ax1.plot(filtered['sample'], filtered['control_expected_loss'], linewidth=0.25, color=control[0].get_color(), alpha=0.3)
            ax1.plot(filtered['sample'], filtered['treatment_expected_loss'], linewidth=0.25, color=treatment[0].get_color(), alpha=0.3)
            ax2.plot(filtered['sample'], filtered['control_cr'], linewidth=0.25, color=control[0].get_color(), alpha=0.3)
            ax2.plot(filtered['sample'], filtered['treatment_cr'], linewidth=0.25, color=treatment[0].get_color(), alpha=0.3)
        
        
        ax1.set_xlabel('Sample Size')
        ax1.set_ylabel('Expected Loss')
        ax1.set_title('Expected Loss Simulation')
        ax1.legend()
        
        
        ax2.set_xlabel('Sample Size')
        ax2.set_ylabel('Conversion Rates')
        ax2.set_title('Conversion Rates Simulation')
        ax2.legend()
    
    ax1.plot(filtered['sample'], np.full((10000,), 0.0015), label='threshold', linestyle='dashed', color=threshold[0].get_color())

    plt.show()

if __name__ == "__main__":
    plot_peeking_example()

    plot_simulations('experiment_simulations_37.csv')

    
