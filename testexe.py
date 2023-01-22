import win32service
import win32serviceutil
import win32event
import time

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Spotify Keyboard"
    _svc_display_name_ = "Spotify Keyboard"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        x=0
        while True:
            x=x+1
            print(x)
            time.sleep(2)
                    
            if win32event.WaitForSingleObject(self.stop_event, 5000) == win32event.WAIT_OBJECT_0:
                break

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
