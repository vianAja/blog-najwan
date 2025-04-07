import subprocess
from dotenv import load_dotenv
import os

load_dotenv('.creds/.env')

## Credentials for GitLab project
username_gitlab = os.getenv('GITLAB_USERNAME')
password_gitlab = os.getenv('GITLAB_PASSWORD')


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
            'git','push','origin','main'
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    proses_push.stdin.write(f'{username_gitlab}\n{password_gitlab}')
    proses_push.stdin.close()

if __name__ == '__main__':
    print('Masukan Commit Message:')
    input_commit = str(input('  => '))
    push_gitlab(commit_name=input_commit)