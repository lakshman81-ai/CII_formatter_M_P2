import pandas as pd
import subprocess
import io
import sys

def get_table_data(accdb_path, table_name):
    cmd = ["mdb-export", accdb_path, table_name]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return None
    return pd.read_csv(io.StringIO(stdout.decode('utf-8')))

def get_all_tables(accdb_path):
    cmd = ["mdb-tables", accdb_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return []
    tables = stdout.decode('utf-8').strip().split()
    return [t for t in tables if t.startswith('INPUT_')]

def analyze_database(accdb_path):
    print(f"===========================================================")
    print(f" Analyzing Database: {accdb_path} ")
    print(f"===========================================================")
    
    tables = get_all_tables(accdb_path)
    
    # We want to specifically focus on the ones mapped to CII Neutral File auxiliary blocks
    key_tables = [
        "INPUT_BASIC_ELEMENT_DATA", "INPUT_RESTRAINTS", "INPUT_RIGIDS", "INPUT_BENDS",
        "INPUT_DISPLACEMENTS", "INPUT_FORCES", "INPUT_UNIFORM_LOADS", "INPUT_WIND_LOADS",
        "INPUT_ELEMENT_OFFSETS", "INPUT_ALLOWABLES", "INPUT_FLANGES", "INPUT_SIFTEES",
        "INPUT_REDUCERS", "INPUT_EXPANSION_JOINTS", "INPUT_STRUCTURAL_STEEL_SECTIONS",
        "INPUT_EQUIPMENT", "INPUT_COORD_SYSTEMS"
    ]
    
    for t in key_tables:
        if t not in tables:
            continue
        df = get_table_data(accdb_path, t)
        if df is None or df.empty:
            continue
            
        print(f"\n--- Table: {t} ---")
        
        default_cols = []
        mandatory_cols = []
        
        for col in df.columns:
            # Drop NaN rows just for uniqueness check (or keep to see if it's all NA)
            unique_vals = df[col].dropna().unique()
            
            if len(unique_vals) == 0:
                default_cols.append(f"{col} (All Empty/NA)")
            elif len(unique_vals) == 1:
                val = unique_vals[0]
                if isinstance(val, float) and round(val, 4) == -1.0101:
                    default_cols.append(f"{col} (CAESAR Calculated Default: -1.0101)")
                elif val == 0 or val == 0.0 or val == "0" or val == "0.0":
                    default_cols.append(f"{col} (Zero: {val})")
                elif val == False or val == "False":
                    default_cols.append(f"{col} (False)")
                elif str(val).strip() == "" or str(val).strip() == "-1":
                    default_cols.append(f"{col} (Empty/Unassigned: '{val}')")
                else:
                    default_cols.append(f"{col} (Constant value: {val})")
            else:
                mandatory_cols.append(col)
                
        print(f"Mandatory Columns ({len(mandatory_cols)}):")
        print("  " + ", ".join(mandatory_cols))
        print(f"\nDefault/Config/Constant Columns ({len(default_cols)}):")
        for d in default_cols:
            print("  - " + d)

if __name__ == "__main__":
    analyze_database("SAMPLE2.ACCDB")
    analyze_database("INLET-SEPARATOR-SKID-C2.ACCDB")
