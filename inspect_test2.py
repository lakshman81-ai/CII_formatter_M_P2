import pandas as pd
from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings
from exporter import generate_custom_csv
from importer import reconstruct_from_csv
import difflib

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

print("EL 0 REL RAW:", len(data["elements"][0]["REL_RAW"]))

df = generate_custom_csv(data, "test_full.csv")
data2 = reconstruct_from_csv("test_full.csv", data)

print("EL 0 REL RAW after:", len(data2["elements"][0]["REL_RAW"]))
print("EL 0 REL RAW[2] after:", repr(data2["elements"][0]["REL_RAW"][2]))
