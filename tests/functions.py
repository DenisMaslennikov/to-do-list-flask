import socket
import time


def wait_for_port(host, port, timeout=60):
    """Ожидание открытия порта на указанном хосте."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    return False
