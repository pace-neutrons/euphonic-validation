import os
import fnmatch

def find_file(fdir, pattern):
    for f in os.listdir(fdir):
        if fnmatch.fnmatch(f, pattern):
            return os.path.join(fdir, f)
    raise Exception(f'{pattern} not found in {fdir}')
