
import sys

def print_log(outStr, verbose=True):
    if verbose:
        sys.stdout.write(outStr)
    sys.stdout.flush()
