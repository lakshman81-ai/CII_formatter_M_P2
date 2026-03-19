import pandas as pd
from typing import Dict, Any, List
import copy
from logger import get_logger

logger = get_logger("importer")

def reconstruct_from_csv(csv_path: str, base_parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes an existing parsed .cii dictionary and merges edits from the provided 41-column CSV.
    Uses the original `base_parsed_data` as the foundation, preserving `REL_RAW`, `IEL_RAW`,
    and `STR_RAW` strings for unchanged values.
    Only modifies the parsed values and strips the RAW string at that specific index if changed.
    """
    logger.info(f"[IMPORT] Merging elements from CSV table: {csv_path}")

    try:
        if isinstance(csv_path, pd.DataFrame):
            df = csv_path
        else:
            df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"[IMPORT] Failed to read CSV: {e}")
        return base_parsed_data

    original_elements = base_parsed_data.get("elements", [])
    new_elements = []

    # Check if number of elements matches. For this MVP, we assume a 1:1 row mapping.
    # If the CSV has more/fewer rows, we'd need more complex diffing.

    for idx, row in df.iterrows():
        if idx < len(original_elements):
            el = copy.deepcopy(original_elements[idx])
        else:
            el = {
                "REL": [0.0] * 98,
                "IEL": [0] * 18,
                "STR": ["", ""],
                "REL_RAW": [],
                "IEL_RAW": [],
                "STR_RAW": []
            }

        def update_rel(index, new_val):
            try:
                # Compare as float (with small tolerance)
                orig_val = float(el["REL"][index]) if len(el["REL"]) > index else 0.0
                if abs(float(new_val) - orig_val) > 1e-6:
                    # Value changed! Update it.
                    while len(el["REL"]) <= index: el["REL"].append(0.0)
                    el["REL"][index] = float(new_val)

                    # We need to invalidate the RAW string for the line containing this value.
                    # REL values are printed 6 per line.
                    line_idx = index // 6
                    if "REL_RAW" in el and len(el["REL_RAW"]) > line_idx:
                        el["REL_RAW"][line_idx] = None  # None signals the serializer to re-format this line
            except Exception as e:
                pass

        def update_iel(index, new_val):
            try:
                orig_val = int(el["IEL"][index]) if len(el["IEL"]) > index else 0
                if int(new_val) != orig_val:
                    while len(el["IEL"]) <= index: el["IEL"].append(0)
                    el["IEL"][index] = int(new_val)
                    line_idx = index // 6
                    if "IEL_RAW" in el and len(el["IEL_RAW"]) > line_idx:
                        el["IEL_RAW"][line_idx] = None
            except Exception as e:
                pass

        def update_str(index, new_val):
            try:
                orig_val = el["STR"][index] if len(el["STR"]) > index else ""
                if str(new_val) != orig_val:
                    while len(el["STR"]) <= index: el["STR"].append("")
                    el["STR"][index] = str(new_val)
                    line_idx = index // 6
                    if "STR_RAW" in el and len(el["STR_RAW"]) > line_idx:
                        el["STR_RAW"][line_idx] = None
            except Exception as e:
                pass

        # Parse CSV values
        text = str(row.get("TEXT", ""))
        nodes = text.split(" ")[-1].split("-") if " " in text and "-" in text else ["0", "0"]
        try:
            update_rel(0, float(nodes[0]))
            update_rel(1, float(nodes[1]))
        except:
            pass

        update_rel(2, row.get("DELTA_X", 0.0))
        update_rel(3, row.get("DELTA_Y", 0.0))
        update_rel(4, row.get("DELTA_Z", 0.0))

        update_rel(5, row.get("DIAMETER", 0.0))
        update_rel(6, row.get("WALL_THICK", 0.0))

        update_str(1, str(row.get("PIPELINE-REFERENCE", "")))

        for ptr_name, idx_iel in [("BEND_PTR", 0), ("RIGID_PTR", 1), ("INT_PTR", 10)]:
            val = row.get(ptr_name, 0)
            if pd.isna(val): val = 0
            update_iel(idx_iel, val)

        comp_type = str(row.get("Type", ""))
        if comp_type == "Support":
            update_iel(3, 1) # Restraint pointer generic fallback

        new_elements.append(el)

    base_parsed_data["elements"] = new_elements
    base_parsed_data["control"]["NUMELT"] = len(new_elements)

    logger.info(f"[IMPORT] Successfully merged {len(new_elements)} elements from CSV.")
    return base_parsed_data
