import psutil
import platform

from megumin import Config

from distutils.version import LooseVersion

def check_requirements():
    # Verifica a quantidade de RAM
    ram = psutil.virtual_memory().total / (1024 ** 3)  # em GB
    if ram < Config.RAM_CHECK:
        print(ram)
        return False

    # Verifica a velocidade do processador
    freq = psutil.cpu_freq().current  # em MHz
    if freq < Config.CPU_MHZ_CHECK:
        print(freq)
        return False

    # Verifica a versão do sistema operacional
    version = platform.release()
    if LooseVersion(version) < LooseVersion(Config.MIN_SYSTEM):
        print(LooseVersion(version))
        return False

    # Verifica o espaço livre em disco
    disk = psutil.disk_usage('/').free / (1024 ** 3)  # em GB
    if disk < Config.STORAGE_CHECK:
        print(disk)
        return False

    return True

