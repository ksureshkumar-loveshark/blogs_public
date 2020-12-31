import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import beta
import matplotlib.pyplot as plt
import json
import decimal
decimal.getcontext().prec = 4
from generate_experiment_data import CONTROL_SIZE, TREATMENT_SIZE

def calculate_expected_loss(control_simulation, treatment_simulation, treatment_won):
    loss_control = [max(j - i, 0) for i,j in zip(control_simulation, treatment_simulation)]
    loss_treatment = [max(i - j, 0) for i,j in zip(control_simulation, treatment_simulation)]

    all_loss_control = [int(i)*j for i,j in zip(treatment_won, loss_control)]
    all_loss_treatment = [(1 - int(i))*j for i,j in zip(treatment_won, loss_treatment)]

    expected_loss_control = np.mean(all_loss_control)
    expected_loss_treatment = np.mean(all_loss_treatment)
    return expected_loss_control, expected_loss_treatment

if __name__ == "__main__":
    experiment_data = pd.read_csv('experiment_data.csv')

    print(experiment_data.head())
    print(experiment_data.shape)

    results = experiment_data.groupby('group').agg({'userId': pd.Series.nunique, 'converted': sum})
    results.rename({'userId': 'sampleSize'}, axis=1, inplace=True)
    results['conversionRate'] = results['converted']/results['sampleSize']

    print(results)

    control = beta(7 + results.loc['control', 'converted'], 15 + results.loc['control', 'sampleSize'] - results.loc['control', 'converted'])
    treatment = beta(7 + results.loc['treatment', 'converted'], 15 + results.loc['treatment', 'sampleSize'] - results.loc['treatment', 'converted'])


    # fig, ax = plt.subplots()

    # x = np.linspace(0,1,1000)

    # ax.plot(x, control.pdf(x), label='control')
    # ax.plot(x, treatment.pdf(x), label='treatment')
    # ax.set_xlabel('Conversion Probability')
    # ax.set_ylabel('Density')
    # ax.set_title('Experiment Posteriors')
    # ax.legend()
    # plt.show()

    joint_dist_for_plot = []
    for i in np.linspace(0.26,0.42,161):
        for j in np.linspace(0.26,0.42,161):
            joint_dist_for_plot.append([i, j, control.pdf(i)*treatment.pdf(j)])

    joint_dist_for_plot = pd.DataFrame(joint_dist_for_plot)
    joint_dist_for_plot.rename({0: 'control_cr', 1: 'treatment_cr', 2: 'joint_density'}, axis=1, inplace=True)
    tick_locations = range(0, 160, 10)
    tick_labels = [round(0.26 + i*0.01, 2) for i in range(16)]
    heatmap_df = pd.pivot_table(joint_dist_for_plot, values='joint_density', index='treatment_cr', columns='control_cr')
    
    # ax = sns.heatmap(heatmap_df)
    # ax.set_xticks(tick_locations)
    # ax.set_xticklabels(tick_labels)
    # ax.set_yticks(tick_locations)
    # ax.set_yticklabels(tick_labels)
    # ax.invert_yaxis()

    # plt.show()

    control_simulation = np.random.beta(7 + results.loc['control', 'converted'], 15 + results.loc['control', 'sampleSize'] - results.loc['control', 'converted'], size=100000)
    treatment_simulation = np.random.beta(7 + results.loc['treatment', 'converted'], 15 + results.loc['treatment', 'sampleSize'] - results.loc['treatment', 'converted'], size=100000)

    treatment_won = [i <= j for i,j in zip(control_simulation, treatment_simulation)]

    chance_to_beat_ctrl = np.mean(treatment_won)
    control_wins = len(treatment_won) - sum(treatment_won)
    treatment_wins = sum(treatment_won)

    print(chance_to_beat_ctrl, control_wins, treatment_wins)

    expected_loss_control, expected_loss_treatment = calculate_expected_loss(control_simulation, treatment_simulation, treatment_won)

    print(f'Expected loss of choosing control: {decimal.getcontext().create_decimal(expected_loss_control)}. Expected loss of choosing treatment: {decimal.getcontext().create_decimal(expected_loss_treatment)}')

