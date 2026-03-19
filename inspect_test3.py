import difflib

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.read()

with open('test_full.csv', 'r') as f:
    pass

# Read debug out from previous run
with open('debug_out.cii', 'r', encoding='latin-1') as f:
    gen = f.read()

diff = list(difflib.unified_diff(orig.splitlines(), gen.splitlines(), n=0))
# Let's see what is failing
for i, l in enumerate(diff):
    if "@@" in l:
        print("\n" + "".join(diff[i:i+4]))
