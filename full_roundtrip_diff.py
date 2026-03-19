import pandas as pd
from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings
from exporter import generate_custom_csv
from importer import reconstruct_from_csv
import difflib

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.read()

# 1. Export
df = generate_custom_csv(data, "test_full.csv")

# 2. Import back
data2 = reconstruct_from_csv("test_full.csv", data)

# 3. Serialize
s_settings = SerializerSettings(use_dos_newlines='\r\n' in orig)
serializer = CIISerializer(s_settings)
gen_str = serializer.serialize(data2)

# Compare
diff = list(difflib.unified_diff(orig.splitlines(True), gen_str.splitlines(True), n=0))
print(f"Diff lines: {len(diff)}")
if diff:
    print("".join(diff[:50]))
