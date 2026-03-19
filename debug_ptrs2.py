import pandas as pd
from parser import CIIParser, ParserSettings

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

print(f"BEND len: {len(data['aux_data']['BEND'])}")
print(f"BEND type: {type(data['aux_data']['BEND'])}")
for i, item in enumerate(data['aux_data']['BEND']):
    print(f"BEND item {i} type: {type(item)}")
    print(f"BEND item {i} len: {len(item)}")
