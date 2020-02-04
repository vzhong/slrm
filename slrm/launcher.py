import os
import shutil
import subprocess


default_args = {
    'job-name': 'slrm-job',
    'nodes': 1,
    'gpus': 0,
    'cpus-per-task': 1,
    'ntasks': 1,
    'time': '1:00:00',
    'mem': '32G',
    'chdir': os.getcwd(),
    # 'mail-type': 'ALL',
    'export': 'all',
}


def verbose_print(verbose, *args, **kwargs):
    if verbose:
        print(*args, **kwargs)


def make_slurm_batch(cmd, dout, slurm_kwargs, fbatch):
    args = default_args.copy()
    args.update(slurm_kwargs)
    args.update(dict(error=os.path.join(dout, 'slurm.err'), output=os.path.join(dout, 'slurm.out')))

    lines = ['#!/usr/bin/env bash']
    for k, v in args.items():
        lines.append('#SBATCH --{key}={val}'.format(key=k, val=v))
    lines.append(cmd)
    if not os.path.isdir(os.path.dirname(fbatch)):
        os.makedirs(os.path.dirname(fbatch))
    with open(fbatch, 'wt') as f:
        f.write('\n'.join(lines) + '\n')


def launch(cmd, slurm_kwargs, dout=os.getcwd(), dry=False, stdout=None, stderr=None, verbose=True):
    # make slurm file
    fbatch = os.path.join(dout, 'slurm.batch')
    make_slurm_batch(cmd, dout, slurm_kwargs, fbatch)
    verbose_print('Created Slurm Batch file at {}'.format(fbatch))

    # do subprocess call
    if dry:
        verbose_print(verbose, '>>> Running job locally')
        verbose_print(verbose, cmd)
        return subprocess.run(cmd.split(), stdout=stdout, stderr=stderr, check=True)
    else:
        slurm_cmd = ['sbatch', fbatch]
        out = subprocess.run(slurm_cmd, check=True, stdout=subprocess.PIPE)
        try:
            job_id = int(out.stdout.strip().split()[-1])
        except:
            raise Exception('Could not parse sbatch output: {}'.format(out.stdout))
        else:
            print(out.stdout.decode())
            with open(os.path.join(dout, 'slurm.jobid'), 'wt') as f:
                f.write(str(job_id))
        return out
