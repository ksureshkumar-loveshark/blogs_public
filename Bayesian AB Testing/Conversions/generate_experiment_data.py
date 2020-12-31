import pandas as pd
import numpy as np
import uuid

CONTROL_SIZE = 2743
CONTROL_CONVERSION_PROBABILITY = 0.326

TREATMENT_SIZE = 2358
TREATMENT_CONVERSION_PROBABILITY = 0.345


if __name__ == "__main__":
    control_user_ids = [uuid.uuid4().hex for i in range(CONTROL_SIZE)]
    control_conversion_flips = np.random.uniform(0,1,CONTROL_SIZE)
    control_converted = [i <= CONTROL_CONVERSION_PROBABILITY for i in control_conversion_flips]
    
    control = pd.DataFrame()
    control['userId'] = control_user_ids
    control['group'] = 'control'
    control['converted'] = control_converted

    treatment_user_ids = [uuid.uuid4().hex for i in range(TREATMENT_SIZE)]
    treatment_conversion_flips = np.random.uniform(0,1,TREATMENT_SIZE)
    treatment_converted = [i <= TREATMENT_CONVERSION_PROBABILITY for i in treatment_conversion_flips]
    
    treatment = pd.DataFrame()
    treatment['userId'] = treatment_user_ids
    treatment['group'] = 'treatment'
    treatment['converted'] = treatment_converted

    results = pd.concat([control, treatment])
    results = results.sample(frac=1)
    results.to_csv('experiment_data.csv', index=False)