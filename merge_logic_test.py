import json
def merge_element(orig_el, row):
    # Map CSV row back to REL indices
    # We only overwrite if value differs!
    # Problem: CSV values are floats. Original values might be float, but text was inherited "0.0000" vs "" vs " 1.2"
    pass
