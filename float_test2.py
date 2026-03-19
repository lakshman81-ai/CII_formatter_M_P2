def update_rel(orig_val, new_val):
    new_fval = float(new_val)
    diff = abs(new_fval - orig_val)
    # The current code uses > 1e-6
    return diff > 1e-6

print(update_rel(0.0000499901, "0.00005"))
