import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import beta, gamma

if __name__ == '__main__':

    prior_data = pd.read_csv('prior_data_conversions.csv')

    successes = prior_data['converted'].sum()
    failures = prior_data.shape[0] - successes

    x = np.linspace(0,1,1000)

    true_prior = beta(successes + 1, failures + 1)

    partitions = np.array_split(prior_data, 100)

    rates = []

    for partition in partitions:
        rates.append(partition['converted'].mean())

    _, ax = plt.subplots()

    sns.histplot(rates, kde=True, label='CR')
    ax.plot(x, true_prior.pdf(x), label='True Prior')
    ax.legend()
    ax.set_xlabel('Conversion Rate')
    ax.set_ylabel('Density')
    ax.set_title('Histogram of Prior Conversion Rates')
    plt.show()