import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

def plot_delta_simulations():
    _, ax = plt.subplots()

    percentage_mappings = {2: '5', 5: '15', 9:'30'}

    for mte in [2, 5, 9]:
        simulations = pd.read_csv(f'experiment_simulations_{32 + mte}.csv')

        simulations = simulations[simulations['winner'] != 'inconclusive']
        
        simulations = simulations[simulations['sample'] >= 200]

        grouped = simulations[['simulation', 'sample']].groupby('simulation', as_index=False).min()

        results = simulations.merge(grouped, on=['simulation', 'sample'])

        hist = results[['simulation', 'sample']].groupby('sample', as_index=False).count()

        records = json.loads(hist.set_index('sample').to_json(orient='index'))

        conclusive_simulations = 0
        print_counter = 0
        plotting_conclusions = []
        x = list(range(1, 10001))

        for i in x:
            if str(i) in records:
                conclusive_simulations += records[str(i)]['simulation']

            if (conclusive_simulations >= 80) and (print_counter < 1):
                print(f'For minimum detectable effect of {percentage_mappings[mte]}%, {80}% of simulations needed {i} samples to be conclusive')
                print_counter += 1

            plotting_conclusions.append(conclusive_simulations)

        ax.plot(x, plotting_conclusions, label=f'{percentage_mappings[mte]}%')

    ax.plot(list(range(1,10001)), np.full((10000,), 80), label='80% threshold', linestyle='dashed')
    ax.legend()
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Proportion of Conclusive Simulations')
    ax.set_title('Conclusive Simulations for varying δ')

    plt.show()


def plot_epsilon_simulations():
    _, ax = plt.subplots()

    sim_names = {'low': 'low_eps',
                 'medium': '37',
                 'high': 'high_eps'}

    epsilons = {'low': 0.0005,
                 'medium': 0.0015,
                 'high': 0.003}

    for eps in ['low', 'medium', 'high']:
        simulations = pd.read_csv(f'experiment_simulations_{sim_names[eps]}.csv')

        simulations = simulations[simulations['winner'] != 'inconclusive']
        
        simulations = simulations[simulations['sample'] >= 200]

        grouped = simulations[['simulation', 'sample']].groupby('simulation', as_index=False).min()

        results = simulations.merge(grouped, on=['simulation', 'sample'])

        hist = results[['simulation', 'sample']].groupby('sample', as_index=False).count()

        records = json.loads(hist.set_index('sample').to_json(orient='index'))

        conclusive_simulations = 0
        print_counter = 0
        plotting_conclusions = []
        x = list(range(1, 10001))

        for i in x:
            if str(i) in records:
                conclusive_simulations += records[str(i)]['simulation']

            if (conclusive_simulations >= 80) and (print_counter < 1):
                print(f'For minimum detectable effect of {epsilons[eps]}%, {80}% of simulations needed {i} samples to be conclusive')
                print_counter += 1

            plotting_conclusions.append(conclusive_simulations)


        ax.plot(x, plotting_conclusions, label=f'{epsilons[eps]}')

    ax.plot(list(range(1,10001)), np.full((10000,), 80), label='80% threshold', linestyle='dashed')
    ax.legend()
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Proportion of Conclusive Simulations')
    ax.set_title('Conclusive Simulations for varying ϵ')

    plt.show()

def plot_lambda_simulations():
    _, ax = plt.subplots()

    lambda_names = {'low': 'low_lambda',
                    'medium': '37',
                    'high': 'high_lambda'}

    lambdas = {'low': 5,
               'medium': 32,
               'high': 60}

    for cr in lambda_names:

        simulations = pd.read_csv(f'experiment_simulations_{lambda_names[cr]}.csv')

        simulations = simulations[simulations['winner'] != 'inconclusive']
        
        simulations = simulations[simulations['sample'] >= 200]

        grouped = simulations[['simulation', 'sample']].groupby('simulation', as_index=False).min()

        results = simulations.merge(grouped, on=['simulation', 'sample'])

        hist = results[['simulation', 'sample']].groupby('sample', as_index=False).count()

        records = json.loads(hist.set_index('sample').to_json(orient='index'))

        conclusive_simulations = 0
        print_counter = 0
        plotting_conclusions = []
        x = list(range(1, 10001))

        for i in x:
            if str(i) in records:
                conclusive_simulations += records[str(i)]['simulation']

            if (conclusive_simulations >= 80) and (print_counter < 1):
                print(f'For minimum detectable effect of {lambdas[cr]}%, {80}% of simulations needed {i} samples to be conclusive')
                print_counter += 1

            plotting_conclusions.append(conclusive_simulations)


        ax.plot(x, plotting_conclusions, label=f'{lambdas[cr]}%')
    
    ax.plot(list(range(1,10001)), np.full((10000,), 80), label='80% threshold', linestyle='dashed')

    ax.legend()
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Proportion of Conclusive Simulations')
    ax.set_title('Conclusive Simulations for varying λ')
    
    plt.show()



if __name__ == "__main__":
    
    plot_delta_simulations()

    plot_epsilon_simulations()

    plot_lambda_simulations()

    

    



    

    

