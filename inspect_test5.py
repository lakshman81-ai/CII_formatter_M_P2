import pandas as pd
from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings
from exporter import generate_custom_csv
from importer import reconstruct_from_csv

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')
df = generate_custom_csv(data, "test_full.csv")
data2 = reconstruct_from_csv("test_full.csv", data)

rel_raw = data2['elements'][0]['REL_RAW']
print("rel_raw:", repr(rel_raw))
print("all instance string?:", all(isinstance(x, str) and len(x) > 20 for x in rel_raw))
