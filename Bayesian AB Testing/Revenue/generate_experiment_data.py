import pandas as pd
import numpy as np
import uuid

CONTROL_SIZE = 2743
CONTROL_CONVERSION_PROBABILITY = 0.326
CONTROL_REVENUE_RATE = 2.0

TREATMENT_SIZE = 2358
TREATMENT_CONVERSION_PROBABILITY = 0.329
TREATMENT_REVENUE_RATE = 1.2

if __name__ == "__main__":
    control_user_ids = [uuid.uuid4().hex for i in range(CONTROL_SIZE)]
    control_conversion_flips = np.random.binomial(n=1, p=CONTROL_CONVERSION_PROBABILITY, size=CONTROL_SIZE)

    control_data = pd.DataFrame()
    control_data['userId'] = control_user_ids
    control_data['group'] = 'control'
    control_data['converted'] = control_conversion_flips

    control_converted = control_data[control_data['converted'] == 1]
    control_no_of_conversions = control_converted.shape[0]
    control_revenue = np.random.exponential(scale=1/CONTROL_REVENUE_RATE, size=control_no_of_conversions)
    control_converted['revenue'] = control_revenue

    control_rest = control_data[control_data['converted'] == 0]
    control_rest['revenue'] = 0

    control_data = pd.concat([control_converted, control_rest])
    control_data = control_data.sample(frac=1)
    control_data = control_data.round(decimals=2)


    treatment_user_ids = [uuid.uuid4().hex for i in range(TREATMENT_SIZE)]
    treatment_conversion_flips = np.random.binomial(n=1, p=TREATMENT_CONVERSION_PROBABILITY, size=TREATMENT_SIZE)

    treatment_data = pd.DataFrame()
    treatment_data['userId'] = treatment_user_ids
    treatment_data['group'] = 'treatment'
    treatment_data['converted'] = treatment_conversion_flips

    treatment_converted = treatment_data[treatment_data['converted'] == 1]
    treatment_no_of_conversions = treatment_converted.shape[0]
    treatment_revenue = np.random.exponential(scale=1/TREATMENT_REVENUE_RATE, size=treatment_no_of_conversions)
    treatment_converted['revenue'] = treatment_revenue

    treatment_rest = treatment_data[treatment_data['converted'] == 0]
    treatment_rest['revenue'] = 0

    treatment_data = pd.concat([treatment_converted, treatment_rest])
    treatment_data = treatment_data.sample(frac=1)
    treatment_data = treatment_data.round(decimals=2)

    experiment_data = pd.concat([control_data, treatment_data])
    experiment_data = experiment_data.sample(frac=1)
    experiment_data.to_csv('experiment_data.csv', index=False)