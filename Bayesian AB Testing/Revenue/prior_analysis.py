import pandas as pd
import numpy as np
from scipy.stats import gamma
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    prior_data = pd.read_csv('prior_data.csv')

    print(prior_data.head())
    print(prior_data.shape)

    conversion_rate = prior_data['converted'].sum()/prior_data.shape[0]
    converted = prior_data[prior_data['converted'] == 1]
    avg_purchase = converted['revenue'].mean()
    print(f'Prior Conversion Rate is {round(conversion_rate, 3)}. Average Revenue per Sale is {round(avg_purchase, 3)}.')
    print(f'Revenue Rate is {round(1/avg_purchase, 3)}. Average Revenue per User is {round(conversion_rate*avg_purchase, 3)}.')

    prior_weak = gamma(a=0.1, scale=0.1)
    prior_mid = gamma(a=2, scale=2)
    prior_strong = gamma(a=2, scale=1)

    fig, ax = plt.subplots(1, 1)

    x = list(range(20))
    y_weak = [prior_weak.pdf(i) for i in x]
    y_mid = [prior_mid.pdf(i) for i in x]
    y_strong = [prior_strong.pdf(i) for i in x]

    # sns.histplot(data=converted['revenue'], stat='probability')
    # sns.lineplot(x=x, y=y_weak, palette='tab10', label='weak Γ(0.2, 0.2)')
    # sns.lineplot(x=x, y=y_mid, palette='tab10', label='mid Γ(2, 2)')
    # sns.lineplot(x=x, y=y_strong, palette='tab10', label='strong Γ(2, 1)')
    # ax.set_xlabel('Revenue')
    # ax.set_ylabel('Density')
    # ax.set_title('Choice of Priors')

    sns.lineplot(x=x, y=y_weak, palette='tab10', label='prior Γ(0.2, 0.2)')
    ax.set_xlabel('Revenue')
    ax.set_ylabel('Density')
    ax.set_title('Chosen Prior')

    plt.show()