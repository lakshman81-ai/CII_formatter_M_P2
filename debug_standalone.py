from importer import reconstruct_from_csv
import pandas as pd

df = pd.DataFrame([{"TEXT": "Pipe 10-20", "IEL_00": 1, "IEL_01": 2}])
# Test the is_standalone check
try:
    data = reconstruct_from_csv(df, None)
except Exception as e:
    print(f"Error: {e}")
