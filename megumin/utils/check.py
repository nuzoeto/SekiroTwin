import psutil
import platform

from megumin import Config

from distutils.version import LooseVersion

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
    if 'microsoft' in platform.uname().release.lower():
        # Executando no Ubuntu no WSL
        if LooseVersion(version.split('-')[0]) < LooseVersion(Config.WSL_SYSTEM):
            return False
    else:
        # Executando no Ubuntu normal
        if LooseVersion(version) < LooseVersion(Config.MIN_SYSTEM):
            return False

    # Verifica o espaço em disco
    disk = psutil.disk_usage('/').total / (1024 ** 3)  # em GB
    if disk < Config.STORAGE_CHECK:
        return False

    return True

