import pandas as pd
import numpy as np
from scipy.stats import gamma
import uuid

SAMPLE_SIZE = 5268
CONVERSION_PROBABILITY = 0.326
REVENUE_RATE = 2.0

if __name__ == "__main__":
    user_ids = [uuid.uuid4().hex for i in range(SAMPLE_SIZE)]
    conversion_flips = np.random.binomial(n=1, p=CONVERSION_PROBABILITY, size=SAMPLE_SIZE)

    data = pd.DataFrame()
    data['userId'] = user_ids
    data['converted'] = conversion_flips

    converted = data[data['converted'] == 1]
    no_of_conversions = converted.shape[0]
    revenue = np.random.exponential(scale=(1/REVENUE_RATE), size=no_of_conversions)
    converted['revenue'] = revenue

    rest = data[data['converted'] == 0]
    rest['revenue'] = 0

    data = pd.concat([converted, rest])
    data = data.sample(frac=1)
    data = data.round(decimals=2)

    data.to_csv('prior_data.csv', index=False)
