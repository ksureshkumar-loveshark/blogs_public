import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import beta, gamma
import matplotlib.pyplot as plt
import json
from generate_experiment_data import CONTROL_SIZE, TREATMENT_SIZE

def calculate_expected_loss(control_avg_purchase, treatment_avg_purchase, treatment_won):
    loss_control = [max(j - i, 0) for i,j in zip(control_avg_purchase, treatment_avg_purchase)]
    loss_treatment = [max(i - j, 0) for i,j in zip(control_avg_purchase, treatment_avg_purchase)]

    all_loss_control = [int(i)*j for i,j in zip(treatment_won, loss_control)]
    all_loss_treatment = [(1 - int(i))*j for i,j in zip(treatment_won, loss_treatment)]

    expected_loss_control = np.mean(all_loss_control)
    expected_loss_treatment = np.mean(all_loss_treatment)
    return expected_loss_control, expected_loss_treatment


if __name__ == "__main__":
    experiment_data = pd.read_csv('experiment_data.csv')

    print(experiment_data.head())
    print(experiment_data.shape)

    results = experiment_data.groupby('group').agg({'userId': pd.Series.nunique, 'converted': sum, 'revenue': sum})
    results.rename({'userId': 'sampleSize'}, axis=1, inplace=True)
    results['revenuePerSale'] = results['revenue']/results['converted']
    print(results)

    control = gamma(a=(0.1 + results.loc['control', 'converted']), scale=(0.1/(1 + (0.1)*results.loc['control', 'converted']*results.loc['control', 'revenuePerSale'])))
    treatment = gamma(a=(0.1 + results.loc['treatment', 'converted']), scale=(0.1/(1 + (0.1)*results.loc['treatment', 'converted']*results.loc['treatment', 'revenuePerSale'])))

    control_beta = beta(7 + results.loc['control', 'converted'], 15 + results.loc['control', 'sampleSize'] - results.loc['control', 'converted'])
    treatment_beta = beta(7 + results.loc['treatment', 'converted'], 15 + results.loc['treatment', 'sampleSize'] - results.loc['treatment', 'converted'])

    fig, ax = plt.subplots()

    x = np.linspace(0,3,1000)
    # x = np.linspace(0,1,1000)
    # z = [1/i for i in x]

    ax.plot(x, control.pdf(x), label='control')
    ax.plot(x, treatment.pdf(x), label='treatment')
    ax.set_xlabel('Rate Parameter')
    ax.set_ylabel('Density')
    ax.set_title('Experiment Posteriors')
    ax.legend()
    
    # ax.plot(x, control.pdf(z), label='control')
    # ax.plot(x, treatment.pdf(z), label='treatment')
    # ax.set_xlabel('Avg Revenue per Sale')
    # ax.set_ylabel('Density')
    # ax.set_title('Experiment Posteriors')
    # ax.legend()

    # ax.plot(x, control_beta.pdf(x), label='control')
    # ax.plot(x, treatment_beta.pdf(x), label='treatment')
    # ax.set_xlabel('Conversion Probability')
    # ax.set_ylabel('Density')
    # ax.set_title('Experiment Posteriors')
    # ax.legend()

    control_conversion_simulation = np.random.beta(7 + results.loc['control', 'converted'], 15 + results.loc['control', 'sampleSize'] - results.loc['control', 'converted'], size=100000)
    treatment_conversion_simulation = np.random.beta(7 + results.loc['treatment', 'converted'], 15 + results.loc['treatment', 'sampleSize'] - results.loc['treatment', 'converted'], size=100000)

    control_revenue_simulation = np.random.gamma(shape=(0.1 + results.loc['control', 'converted']), scale=(0.1/(1 + (0.1)*results.loc['control', 'converted']*results.loc['control', 'revenuePerSale'])), size=100000)
    treatment_revenue_simulation = np.random.gamma(shape=(0.1 + results.loc['treatment', 'converted']), scale=(0.1/(1 + (0.1)*results.loc['treatment', 'converted']*results.loc['treatment', 'revenuePerSale'])), size=100000)
    
    control_avg_purchase = [i/j for i,j in zip(control_conversion_simulation, control_revenue_simulation)]
    treatment_avg_purchase = [i/j for i,j in zip(treatment_conversion_simulation, treatment_revenue_simulation)]

    treatment_won = [i <= j for i,j in zip(control_avg_purchase, treatment_avg_purchase)]

    chance_to_beat_ctrl = np.mean(treatment_won)
    print(f'Chance of beating control: {round(chance_to_beat_ctrl, 3)}.')

    expected_loss_control, expected_loss_treatment = calculate_expected_loss(control_avg_purchase, treatment_avg_purchase, treatment_won)
    print(f'Expected loss of choosing control: {round(expected_loss_control, 3)}. Expected loss of choosing treatment: {round(expected_loss_treatment, 3)}')


    # ax.hist(control_avg_purchase, density=True, label='control', histtype='stepfilled', bins=100)
    # ax.hist(treatment_avg_purchase, density=True, label='treatment', histtype='stepfilled', bins=100)
    # ax.set_xlabel('Avg Revenue per User')
    # ax.set_ylabel('Density')
    # ax.set_title('Experiment Posteriors')
    # ax.legend()
    plt.show()