def update_rel(orig_val, new_val):
    new_fval = float(new_val)
    diff = abs(new_fval - orig_val)
    print(f"orig: {orig_val}, new: {new_fval}, diff: {diff}")
    # Instead of an absolute tolerance, we should use a relative tolerance for very small numbers, or a stricter tolerance.
    return diff > 1e-6

print(update_rel(0.000965312, 0.000965))
