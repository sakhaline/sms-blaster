import subprocess
import time
from datetime import datetime


def execute_bash(commands):
    """
    executes bash commands
    """
    try:
        for command in commands:
            subprocess.run(command, shell=True, check=True)
            time.sleep(2)
    except subprocess.CalledProcessError as e:
        print(f"BASH ERROR - {e}")


if __name__ == "__main__":
    execute_bash(['echo Test',
                  'git add .',
                  f'git commit -m "autocommit {datetime.utcnow().strftime("%Y_%m_%d__%H_%M")}"',
                  'git push origin develop'])
