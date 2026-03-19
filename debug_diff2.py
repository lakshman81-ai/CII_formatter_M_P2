import pandas as pd
from parser import CIIParser, ParserSettings
from importer import reconstruct_from_csv

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

print("Before merge, len REL_RAW:", len(data['elements'][0]['REL_RAW']))

new_data = reconstruct_from_csv('test.csv', data)

print("After merge, len REL_RAW:", len(new_data['elements'][0]['REL_RAW']))
print("After merge, REL_RAW[1]:", repr(new_data['elements'][0]['REL_RAW'][1]))
