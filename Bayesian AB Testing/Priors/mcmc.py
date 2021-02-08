import arviz as az
import pymc3 as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
az.style.use("arviz-darkgrid")

if __name__ == '__main__':
    prior_revenue = pd.read_csv('prior_data_revenue.csv')

    rev_observed = prior_revenue[prior_revenue['converted'] == 1]['revenue'].values
    conv_observed = prior_revenue['converted'].values

    model = pm.Model()

    with model:
        alpha = pm.Uniform("alpha", lower=0, upper=100)
        beta = pm.Uniform("beta", lower=0, upper=100)
        k = pm.Uniform("k", lower=0, upper=5)
        theta = pm.Uniform("theta", lower=0, upper=5)

        cr = pm.Beta('cr', alpha=alpha, beta=beta)
        rr = pm.Gamma('rr', alpha=k, beta=(1/theta))

        conversion = pm.Bernoulli('conversion', p=cr, observed=conv_observed)
        revenue_per_sale = pm.Exponential('revenue_per_sale', lam=rr, observed=rev_observed)

        trace = pm.sample(10000, return_inferencedata=False)

        az.plot_trace(trace, compact=False)
        plt.show()

