import logging
import sys
import psutil
import subprocess
import time
import warnings

# set up logging and warnings
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

target_file1_full_path = "url\\file1.py"  # please enter url to the file 1
target_file2_full_path = "url\\file2.py"  # please enter url to the file 2


def check_script_running(url_target_script):
    for process in psutil.process_iter(['pid', 'name', "cmdline"]):
        try:
            if process.name().startswith('py') and url_target_script in process.cmdline():
                return True, process.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False, None


def restart_script(url_target_script):
    subprocess.Popen([sys.executable, url_target_script], creationflags=subprocess.CREATE_NEW_CONSOLE)


def main():
    url_target_scripts = (target_file1_full_path,
                          target_file2_full_path)
    check_interval = 30  # in seconds
    logging.basicConfig(level=logging.INFO, format=u'[%(asctime)s] #%(levelname)8s %(message)s')

    while True:
        for url_target_script in url_target_scripts:
            is_running, pid = check_script_running(url_target_script)
            if not is_running:
                logger.info(f"{url_target_script} is not running. Let's reboot it.")
                restart_script(url_target_script)
            else:
                pass
        time.sleep(check_interval)


if __name__ == '__main__':
    main()
