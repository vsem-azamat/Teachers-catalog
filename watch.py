import os
from time import sleep
from subprocess import Popen
from watchgod import watch

def run_bot() -> Popen:
    print("Files changed. Restarting your project...")
    return Popen(['python3', '-m', 'bot'], shell=False)


if __name__ == "__main__":
    watched_dir = os.getcwd()
    process = run_bot()
    for changes in watch(watched_dir):
        if any(change[1].endswith('.py') for change in changes):
            process.terminate()
            sleep(0.1)
            process = run_bot()
