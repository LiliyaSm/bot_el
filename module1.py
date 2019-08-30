from threading import Timer #поточный таймер
import win32api, win32con
from ctypes import windll # решение проблемы с расширением экрана


user32 = windll.user32
user32.SetProcessDPIAware()


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


flag = True

def change_glade():
    flag = True # its time to check another glade
    print ("Doing stuff...")

    return flag

if flag:
    print (time.localtime())
    flag = False

rt = RepeatedTimer(1, change_glade) # it auto-starts, no need of rt.start()