import re

with open('importer.py', 'r') as f:
    code = f.read()

# I see what's happening. `pd.read_csv()` replaces empty string with pd.NA / NaN for numeric columns.
# We also have issues with 0 vs 0.0 comparison. Let's make update_rel and update_iel only fire if explicitly not-NaN and clearly changed.
