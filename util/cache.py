from pathlib import Path

from constant import *

def cache_dict(arr, file_name):
    Path(DATA_PATH).mkdir(parents=True, exist_ok=True)
    with open(Path(DATA_PATH) / file_name, 'w') as f:
        for i, col in enumerate(arr[0].keys()):
            if i != 0:
                f.write(',')
            f.write(str(i))
        f.write('\n')

        for i in arr:
            for j in i.values():
                f.write(j + ',')
            f.write('\n')