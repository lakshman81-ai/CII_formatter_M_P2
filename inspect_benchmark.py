import json

def load_schema():
    with open("ver 11 json.txt", "r") as f:
        return json.load(f)

def read_benchmark():
    with open("SAMPLE 2/BENCHMARK.CII", "rb") as f:
        return f.read().split(b"\r\n")

if __name__ == "__main__":
    lines = read_benchmark()
    print(f"Read {len(lines)} lines from BENCHMARK.CII")
    
    # We will write a generator that emits exact string literals for the boilerplate
    # and generates Fortran formatting code for the elements and other sections
    # Let's inspect the sections
    sections = {}
    current_section = None
    section_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith(b"#$"):
            if current_section:
                sections[current_section] = lines[section_start:i]
            current_section = line.decode('latin-1').strip()
            section_start = i
            
    if current_section:
        sections[current_section] = lines[section_start:]
        
    for k, v in sections.items():
        print(f"Section {k}: {len(v)} lines")
