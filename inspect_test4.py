import difflib

with open('SAMPLE 2/BENCHMARK.CII', 'r', encoding='latin-1') as f:
    orig = f.readlines()

with open('debug_out.cii', 'r', encoding='latin-1') as f:
    gen = f.readlines()

diff = list(difflib.unified_diff(orig, gen, n=0))
# Let's see what is failing
for i, l in enumerate(diff):
    if l.startswith("+") and not l.startswith("+++"):
        # Find which line number in orig this corresponds to
        for j in range(i-1, -1, -1):
            if diff[j].startswith("@@"):
                print("Line context:")
                print(diff[j])
                print("Added line:", l)
                break
        break
