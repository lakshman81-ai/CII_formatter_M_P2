import os
import re

def derive_format(line: str) -> str:
    # Base padding is almost always 2X except for strings or some custom headers
    # Let's analyze spacing and values.
    
    if not line.strip():
        return ""
        
    # Strings check
    if len(line) >= 12 and re.match(r'^\s*\d+\s+.*$', line[:14]):
        # Probably a string length line like (7X, I5, 1X, A)
        # e.g. "             10 unassigned"
        # We can identify strings by character checks, but let's just rely on the common patterns
        # For pure derivation, let's treat it as generic chunks of 13 first if it looks like numbers
        if any(c.isalpha() for c in line[13:]):
            return "STRING_FORMAT"
            
    # If the line appears to be data, calculate the format.
    # It might start with spaces. We will find where the first non-space character is, or assume 2X.
    # A CAESAR line is typically 78 or 80 columns wide.
    # We will literally just chunk it into 13 characters from index 2 to end, and see if it looks numeric.
    if len(line) >= 15:
        data = line[2:]
        chunks = [data[i:i+13] for i in range(0, min(len(data), 78), 13)]
        
        # Are they all numeric (or empty)?
        is_all_numeric = True
        for c in chunks:
            if not c.strip(): continue
            # check if it parses as float
            try:
                float(c.strip())
            except ValueError:
                # Might be 'unassigned' string, check if it's alpha
                if any(x.isalpha() for x in c.strip().lower().replace("e", "")):
                    is_all_numeric = False
                    break
                    
        if is_all_numeric:
            fmt = "(2X"
            for chunk in chunks:
                if not chunk.strip():
                    fmt += f", {len(chunk)}X"
                else:
                    width = len(chunk)
                    if '.' in chunk:
                        decimals = len(chunk.strip()) - (chunk.strip().find('.') + 1)
                        if 'E' in chunk or 'e' in chunk:
                            # To avoid ***, w >= d + 7
                            if width < decimals + 7:
                                decimals = width - 7
                            fmt += f", E{width}.{decimals}"
                        else:
                            fmt += f", F{width}.{decimals}"
                    else:
                        fmt += f", I{width}"
            fmt += ")"
            return fmt
            
    return "CUSTOM_OR_HEADER"


import sys

def analyze_blocks(filename):
    derived_formats = {}
    with open(filename, 'rb') as f:
        content = f.read()
        lines = content.split(b"\r\n") if b"\r\n" in content else content.split(b"\n")

    current_section = "HEADER"
    derived_formats[current_section] = []

    for line_bytes in lines:
        line = line_bytes.decode('latin-1')
        if line.startswith("#$"):
            current_section = line.strip().replace("#$ ", "")
            if current_section not in derived_formats:
                derived_formats[current_section] = []
            continue

        fmt = derive_format(line)
        if fmt and fmt not in derived_formats[current_section]:
            derived_formats[current_section].append(fmt)

    print(f"--- DERIVED FORTRAN FORMATS FOR {filename} ---")
    for block, formats in derived_formats.items():
        if not formats: continue
        print(f"\nBlock: {block}")
        for fmt in formats:
            print(f"  - {fmt}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_blocks(sys.argv[1])
    else:
        analyze_blocks("SAMPLE 2/BENCHMARK.CII")
