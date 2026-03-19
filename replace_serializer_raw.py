import re

with open('serializer.py', 'r') as f:
    content = f.read()

# Make it handle list of lines where some might be None.
# If a line is None, it should format that line from the float/int array instead.

def format_rel_line(rel_array, start_idx, num=6):
    line = " "
    for i in range(start_idx, min(start_idx + num, 98)):
        val = rel_array[i] if i < len(rel_array) else 0.0
        line += " " + f"{val:12.6f}" # A fallback, though CAESAR II uses specific spacing
    return line

# This replacement will be a bit complex to do blindly.
# I will use replace_with_git_merge_diff for precise changes in serializer.py
