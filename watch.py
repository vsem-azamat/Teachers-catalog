from time import sleep
from subprocess import Popen
from watchgod import watch

def run_bot() -> Popen:
    print("Files changed. Restarting your project...")
    return Popen(['venv/bin/python3', '-m', 'bot'], shell=False)


if __name__ == "__main__":
    watched_dir = '/home/poryadok/Projects/teachers_bot'
    process = run_bot()
    for changes in watch(watched_dir):
        if any(change[1].endswith('.py') for change in changes):
            process.terminate()
            sleep(0.1)
            process = run_bot()
