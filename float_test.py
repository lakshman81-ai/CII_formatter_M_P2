def update_rel(orig_val, new_val):
    new_fval = float(new_val)
    diff = abs(new_fval - orig_val)
    print(f"orig: {orig_val}, new: {new_fval}, diff: {diff}")
    return diff > 1e-6

print(update_rel(0.499901E-04, "0.500000E-04"))
