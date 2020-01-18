import os
import slrm


for city, state in [('vancouver', 'bc'), ('toronto', 'on'), ('stanford', 'ca'), ('seattle', 'wa')]:
    cmd = 'python myscript.py --city {} --state {}'.format(city, state)
    slurm_kwargs = {'account': 'cse', 'partition': 'cse-gpu'}
    slrm.launch(cmd, slurm_kwargs, dout=os.path.join('jobs', '{}-{}'.format(city, state)), dry=False)
