import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import beta, gamma

if __name__ == '__main__':
    cr_prior_mean = beta(33, 67)
    cr_prior_map = beta(47, 100)

    x = np.linspace(0,1,1000)

    _, ax = plt.subplots()

    sns.lineplot(x=x, y=cr_prior_mean.pdf(x), label='mean Beta(33, 67)')
    sns.lineplot(x=x, y=cr_prior_map.pdf(x), label='map Beta(47, 100)')
    ax.set_xlabel('Conversion Probability')
    ax.set_ylabel('Density')
    ax.set_title('Conversion Probability Prior')
    ax.legend()

    rr_prior_mean = gamma(a=2.3, scale=2.0)
    rr_prior_map = gamma(a=5, scale=0.4)

    # # x = list(range(20))

    # # rr_mean = [rr_prior_mean.pdf(i) for i in x]
    # # rr_map = [rr_prior_map.pdf(i) for i in x]

    # # sns.lineplot(x=x, y=rr_mean, label='mean Gamma(2.3, 2.0)')
    # # sns.lineplot(x=x, y=rr_map, label='map Gamma(5.0, 0.4)')

    # ax.set_xlabel('Revenue Rate')
    # ax.set_ylabel('Density')
    # ax.set_title('Revenue Rate Prior')
    # ax.legend()

    plt.show()