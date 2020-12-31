import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

if __name__ == "__main__":
    prior_data = pd.read_csv('prior_data.csv')
    
    print(prior_data.head())
    print(prior_data.shape)

    conversion_rate = prior_data['converted'].sum()/prior_data.shape[0]

    print(f'Prior Conversion Rate is {round(conversion_rate, 3)}')

    fig, ax = plt.subplots(1, 1)

    x = np.linspace(0,1,1000)

    # beta_weak = beta(round(conversion_rate, 1)*10 + 1, 10 + 1 - round(conversion_rate, 1)*10)
    # beta_mid = beta(round(conversion_rate, 1)*50 + 1, 50 + 1 - round(conversion_rate, 1)*50)
    # beta_strong = beta(round(conversion_rate, 2)*100 + 1, 100 + 1 - round(conversion_rate, 2)*100)
    prior = beta(round(conversion_rate, 1)*20 + 1, 20 + 1 - round(conversion_rate, 1)*20)

    # ax.plot(x, beta_weak.pdf(x), label=f'weak Beta({int(round(conversion_rate, 1)*10) + 1}, {10 + 1 - int(round(conversion_rate, 1)*10)})')
    # ax.plot(x, beta_mid.pdf(x), label=f'mid Beta({int(round(conversion_rate, 1)*50) + 1}, {50 + 1 - int(round(conversion_rate, 1)*50)})')
    # ax.plot(x, beta_strong.pdf(x), label=f'strong Beta({int(round(conversion_rate, 2)*100) + 1}, {100 + 1 - int(round(conversion_rate, 2)*100)})')
    ax.plot(x, prior.pdf(x), label=f'prior Beta({int(round(conversion_rate, 2)*20) + 1}, {20 + 1 - int(round(conversion_rate, 2)*20)})')
    ax.set_xlabel('Conversion Probability')
    ax.set_ylabel('Density')
    ax.set_title('Chosen Prior')
    ax.legend()
    plt.show()
