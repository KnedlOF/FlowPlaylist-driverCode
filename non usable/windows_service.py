import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import time
i = 0


class MyWindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "windows_service.exe"
    _svc_display_name_ = "SpotifyKeyboard"
    _svc_description_ = "Neki nardi"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Your service code here
        while True:
            i = i+1
            print(i)
            time.sleep(1)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyWindowsService)
