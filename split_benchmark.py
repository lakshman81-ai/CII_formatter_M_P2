import os

import sys

def split_benchmark(input_file, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, "rb") as f:
        content = f.read()
        
    # The file has \r\n line endings. We split by it to get exact lines.
    lines = content.split(b"\r\n") if b"\r\n" in content else content.split(b"\n")
    
    current_section = None
    section_lines = []
    
    def save_section():
        if current_section and section_lines:
            # Make a safe filename
            safe_name = current_section.decode('latin-1').replace("#$", "").strip().lower()
            safe_name = safe_name.replace("&", "_and_")
            filename = os.path.join(output_dir, f"{prefix}_{safe_name}.cii")
            with open(filename, "wb") as out_f:
                # Re-join with original line endings
                ending = b"\r\n" if b"\r\n" in content else b"\n"
                out_f.write(ending.join(section_lines))
                
    for line in lines:
        is_header = False
        if line.startswith(b"#$"):
            is_header = True
        elif len(line) < 25 and line.strip().isalpha():
            is_header = True
        elif len(line) < 25 and b"&" in line and b" " not in line.strip():
            is_header = True
        elif len(line) < 25 and b"_" in line and b" " not in line.strip():
            is_header = True
            
        if is_header:
            save_section()
            # Normalize to match our expected format for output files
            current_section = line.strip().upper()
            if not current_section.startswith(b"#$"):
                current_section = b"#$ " + current_section
            section_lines = [line]
        else:
            if current_section is not None:
                section_lines.append(line)
            else:
                pass
                
    # Save the last section
    save_section()
    
    print(f"Successfully split {input_file} into {output_dir}")
    print("Files created:")
    for f in sorted(os.listdir(output_dir)):
        print(f"  - {f}")

if __name__ == "__main__":
    split_benchmark("SAMPLE 2/BENCHMARK.CII", "benchmark_blocks", "benchmark")
    split_benchmark("INLET-SEPARATOR-SKID-C2.CII", "sample4_blocks", "sample4")
