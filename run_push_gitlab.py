import subprocess
from dotenv import load_dotenv
import os

def push_gitlab(commit_name: str,):
    subprocess.run([
        'git',
        'add',
        '.'
    ], text=False)
    subprocess.run([
        'git','commit','-m',f'"{commit_name}"'
    ], text=False)
    proses_push = subprocess.Popen(
        [
            'git','push','origin','master'
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

if __name__ == '__main__':
    print('Masukan Commit Message:')
    input_commit = str(input('  => '))
    push_gitlab(commit_name=input_commit)