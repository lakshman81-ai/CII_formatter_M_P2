import pandas as pd
from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings
from exporter import generate_custom_csv
from importer import reconstruct_from_csv
from comparator import compare_files
import difflib

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

df = generate_custom_csv(data, 'test.csv')
new_data = reconstruct_from_csv('test.csv', data)

s_settings = SerializerSettings()
serializer = CIISerializer(s_settings)
gen_str = serializer.serialize(new_data)

with open('debug_out.cii', 'w', encoding='latin-1') as f:
    f.write(gen_str)

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.readlines()
with open('debug_out.cii', 'r', encoding='latin-1') as f:
    new_lines = f.readlines()

d = difflib.unified_diff(orig, new_lines, n=0)
diff_lines = list(d)
print("Number of lines changed:", len(diff_lines))
for l in diff_lines[:50]:
    print(repr(l))
