# Let's see what is causing the lines to be different. The diff output shows many zeroes being added.
# Ah, I see: in `serializer.py` it has: `while len(rel) < 98: rel.append(0.0)`. And in `importer.py`
# wait, if the `REL_RAW` is preserved, it should print the raw line.
# Why is `REL_RAW` not printing for the remaining lines? Let's check `len(rel_raw)` in `debug_diff.py`
