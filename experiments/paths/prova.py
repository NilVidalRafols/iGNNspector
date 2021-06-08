import os
from pathlib import Path

path = Path('experiments\\')
path = Path.home()
path = Path.cwd()
l = list(path.glob('.gitignore'))
path2 = Path(l[0])
if path2.is_file():
    print(path2.stat().st_size)

