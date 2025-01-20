import pandas as pd
import numpy as np

# Example: Creating a simple DataFrame
data = {
    'Wallet Address': ['rKtd3FXaE9rcQh5WLy6GGXFUCze5XtA6vS'],
    'Balance': [10000]
}
df = pd.DataFrame(data)
print(df)