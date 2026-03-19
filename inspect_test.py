import difflib

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.readlines()

with open('test_full.csv', 'r') as f:
    pass

# Read debug out from previous run
with open('debug_out.cii', 'r', encoding='latin-1') as f:
    gen = f.readlines()

diff = list(difflib.unified_diff(orig, gen, n=0))
# Let's see what is failing
for i, l in enumerate(diff):
    if "@@" in l:
        print("".join(diff[i:i+6]))
