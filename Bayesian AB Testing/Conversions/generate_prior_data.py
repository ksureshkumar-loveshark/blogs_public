import pandas as pd
import numpy as np
import uuid

SAMPLE_SIZE = 5268
CONVERSION_PROBABILITY = 0.326


if __name__ == "__main__":
    user_ids = [uuid.uuid4().hex for i in range(SAMPLE_SIZE)]
    conversion_flips = np.random.uniform(0,1,SAMPLE_SIZE)
    converted = [i <= CONVERSION_PROBABILITY for i in conversion_flips]
    
    data = pd.DataFrame()
    data['userId'] = user_ids
    data['converted'] = converted 

    data.to_csv('prior_data.csv', index=False)