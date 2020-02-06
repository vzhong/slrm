# slrm

Python library to submit slurm jobs.

Installation:

```
pip install git+https://github.com/vzhong/slrm
```

Usage:

```python
import os
import slrm

for city, state in [('vancouver', 'bc'), ('toronto', 'on'), ('stanford', 'ca'), ('seattle', 'wa')]:
    cmd = 'python myscript.py --city {} --state {}'.format(city, state)
    slurm_kwargs = {'account': 'cse', 'partition': 'cse-gpu'}
    # you can see default args in slrm.launcher.default_args
    slrm.launch(cmd, slurm_kwargs, dout=os.path.join('jobs', '{}-{}'.format(city, state)), dry=False)
```

Pull requests welcome!
