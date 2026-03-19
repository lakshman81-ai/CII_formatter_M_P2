import pandas as pd
from parser import CIIParser, ParserSettings
from importer import reconstruct_from_csv

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

new_data = reconstruct_from_csv('test.csv', data)
for i, el in enumerate(new_data['elements']):
    for j, line in enumerate(el['REL_RAW']):
        if line is None:
            print(f"Element {i} REL_RAW line {j} is None")
