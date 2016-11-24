
import sys

def print_log(out, verbose=True):
    if verbose:
        sys.stdout.write(str(out))
    sys.stdout.flush()
