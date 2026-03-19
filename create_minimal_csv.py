import pandas as pd
from config import MANDATORY_FIELDS

def filter_mandatory_columns(input_csv, output_csv, table_name):
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Skipping {input_csv} (not found)")
        return
        
    mandatory_cols = MANDATORY_FIELDS.get(table_name, [])
    
    if not mandatory_cols:
        print(f"No mandatory columns defined for {table_name}. Exporting all.")
        df.to_csv(output_csv, index=False)
        return
        
    # We must ensure we don't try to pull columns that don't exist 
    # (e.g. if the original table doesn't have it for some reason)
    cols_to_keep = [c for c in mandatory_cols if c in df.columns]
    
    minimal_df = df[cols_to_keep]
    minimal_df.to_csv(output_csv, index=False)
    print(f"Created {output_csv} with {len(cols_to_keep)} mandatory columns (down from {len(df.columns)}).")

if __name__ == "__main__":
    # Create minimal middle layer CSVs
    filter_mandatory_columns("sample4_input_elements.csv", "minimal_elements.csv", "INPUT_BASIC_ELEMENT_DATA")
    filter_mandatory_columns("sample4_input_restraints.csv", "minimal_restraints.csv", "INPUT_RESTRAINTS")
    # For future extension:
    # filter_mandatory_columns("sample4_input_bends.csv", "minimal_bends.csv", "INPUT_BENDS")
    # filter_mandatory_columns("sample4_input_sif_tees.csv", "minimal_sif_tees.csv", "INPUT_SIFTEES")
    # filter_mandatory_columns("sample4_input_allowables.csv", "minimal_allowables.csv", "INPUT_ALLOWABLES")
