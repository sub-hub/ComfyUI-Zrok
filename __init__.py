import subprocess
import atexit
import logging

# @@@@@@@@@@@@@@@@@@@@@ 이 부분 집중 @@@@@@@@@@@@@@@@@@@@@

zrok_reserved_share_token="이곳을_고정된_호스트_name으로_대체"

# @@@@@@@@@@@@@@@@@@@@@ 이 부분 집중 @@@@@@@@@@@@@@@@@@@@@

zrok_command = ["zrok", "share", "reserved", zrok_reserved_share_token]
zrok_process = None

def cleanup_zrok():
    """Function to terminate the zrok process."""
    global zrok_process
    if zrok_process and zrok_process.poll() is None:
        logging.info("Terminating zrok process...")
        zrok_process.terminate()
        try:
            zrok_process.wait(timeout=5)
            logging.info("zrok process terminated.")
        except subprocess.TimeoutExpired:
            logging.warning("zrok process did not terminate gracefully, killing.")
            zrok_process.kill()
            logging.info("zrok process killed.")
try:
    logging.info(f"Starting zrok command: {' '.join(zrok_command)}")
    zrok_process = subprocess.Popen(zrok_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logging.info(f"zrok process started with PID: {zrok_process.pid}")
    atexit.register(cleanup_zrok)
except FileNotFoundError:
    logging.error(f"Error: 'zrok' command not found. Make sure zrok is installed and in your system's PATH.")
except Exception as e:
    logging.error(f"Failed to start zrok process: {e}")
