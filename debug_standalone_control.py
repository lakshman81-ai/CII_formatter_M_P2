import pandas as pd
from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings
from exporter import generate_custom_csv
from importer import reconstruct_from_csv

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

df = generate_custom_csv(data, 'test_standalone.csv')
new_data = reconstruct_from_csv('test_standalone.csv', None)

s_settings = SerializerSettings()
serializer = CIISerializer(s_settings)
gen_str = serializer.serialize(new_data)

# Print CONTROL section of generated string
lines = gen_str.split('\n')
for i, line in enumerate(lines):
    if line.startswith('#$ CONTROL'):
        for j in range(5):
            print(lines[i+j])
        break
