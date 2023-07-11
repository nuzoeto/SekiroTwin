import psutil
import platform

from megumin import Config

def check_requirements():
    # Verifica a quantidade de RAM
    ram = psutil.virtual_memory().total / (1024 ** 3)  # em GB
    if ram < Config.RAM_CHECK:
        return False

    # Verifica a velocidade do processador
    freq = psutil.cpu_freq().current  # em MHz
    if freq < Config.CPU_MHZ_CHECK:
        return False

    # Verifica a versão do sistema operacional
    version = platform.release()
    if version < Config.MIN_SYSTEM:
        return False

    # Verifica o espaço livre em disco
    disk = psutil.disk_usage('/').free / (1024 ** 3)  # em GB
    if disk < Config.STORAGE_CHECK:
        return False

    return True

