import difflib
from parser import CIIParser, ParserSettings
from serializer import CIISerializer, SerializerSettings

settings = ParserSettings(n1_base=2000, is_data_matrix=False)
p = CIIParser(settings)
data = p.parse('SAMPLE 2/BENCHMARK.CII')

s_settings = SerializerSettings(use_dos_newlines=True)
serializer = CIISerializer(s_settings)
gen_str = serializer.serialize(data)

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.read()

diff = list(difflib.unified_diff(orig.splitlines(True), gen_str.splitlines(True), n=0))
print("".join(diff[:30]))
