import sys

def lines_with_index(lines):
    return [f"{i}: {line}" for i, line in enumerate(lines)]

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.read().split('\n')

with open('debug_out.cii', 'r', encoding='latin-1') as f:
    gen = f.read().split('\n')

for i in range(min(len(orig), len(gen))):
    if orig[i] != gen[i]:
        print(f"First mismatch at line {i}:")
        print(f"Orig: {repr(orig[i])}")
        print(f"Gen:  {repr(gen[i])}")
        break
