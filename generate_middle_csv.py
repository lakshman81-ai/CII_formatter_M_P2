import pandas as pd
import argparse
from config import MANDATORY_COLUMNS

def create_middle_csv(output_path: str):
    df = pd.DataFrame(columns=MANDATORY_COLUMNS)
    df.to_csv(output_path, index=False)
    print(f"✅ Middle-layer template created at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="middle_layer_template.csv")
    args = parser.parse_args()
    create_middle_csv(args.output)
