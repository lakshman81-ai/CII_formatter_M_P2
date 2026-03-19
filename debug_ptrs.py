import pandas as pd
from parser import CIIParser, ParserSettings
from importer import reconstruct_from_csv

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

for key, val in data['aux_data'].items():
    print(f"{key} original len: {len(val)}")
