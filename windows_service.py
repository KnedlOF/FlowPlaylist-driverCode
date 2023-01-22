import win32serviceutil
import win32service
import sys
import subprocess


def find_python_exe():
    python_exe = sys.executable
    return python_exe


def run_service():
    win32serviceutil.StartService("Spotify keyboard")

def check_service_status():
    output = subprocess.check_output(['sc', 'query', 'Spotify keyboard'])
    if 'RUNNING' in output.decode():
        print('Service is running')
    else:
        print('Service is not running')

def install_service():
    win32serviceutil.InstallService(
        'Spotify keyboard',  # Service Name
        'Spotify keyboard',  # Display Name
        'Spotify keyboard',  # Description
        startType=win32service.SERVICE_AUTO_START,
        exeName='testexe.exe'   # path to the python interpreter
    )
    print("Service Installed")

def check_if_installed(service_name):
    try:
        status = win32serviceutil.QueryServiceStatus(service_name)
        return True
    except win32service.error as e:
        if e.winerror == 1060:  # ERROR_SERVICE_DOES_NOT_EXIST
            return False
        else:
            raise


if check_if_installed('Spotify keyboard'):
    print('Service is already installed')
    run_service()
    check_service_status()
else:
    print('Service is not installed')
    install_service()
    run_service()
    check_service_status()







