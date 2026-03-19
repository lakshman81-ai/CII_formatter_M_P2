import pandas as pd
from parser import CIIParser, ParserSettings
from importer import reconstruct_from_csv

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

df = pd.read_csv('test_standalone.csv')
for i, el in enumerate(data['elements']):
    orig_val = float(el["REL"][12])
    new_fval = float(df.loc[i, "REL_12"])
    print(f"orig: {orig_val}, new: {new_fval}, diff: {abs(new_fval - orig_val)}")
