import win32com.client
import win32api, win32con
import random

class Mouse(object):
    def __init__(self):
        self.x_res = win32api.GetSystemMetrics(0)
        self.y_res = win32api.GetSystemMetrics(1)

    def left_click(self, x, y):
        nx = int(x*65535/self.x_res)
        ny = int(y*65535/self.y_res)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
        n = random.randint(1700,2000) 
        print(n)
        win32api.Sleep(n)   
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_ABSOLUTE,x,y,0,0)
        win32api.Sleep(400)
        print("click")
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP|win32con.MOUSEEVENTF_ABSOLUTE,x,y,0,0)#completely optional. But nice for debugging purposes.
        win32api.Sleep(200)

    def move(self, x, y):
        nx = int(x*65535/self.x_res)
        ny = int(y*65535/self.y_res)

        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
        win32api.Sleep(200)

    def drag(self, x, y, x_next, y_next, release):
        nx = int(x*65535/self.x_res)
        ny = int(y*65535/self.y_res)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
        n = random.randint(700,800) 
        #time.sleep(5)
        win32api.Sleep(n)   
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_ABSOLUTE,x,y,0,0)
        win32api.Sleep(200)
        self.move(x_next, y_next)
        if release:
            win32api.Sleep(150)
            win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP,x, y, 0, 0)

    def left_up(self):                
        win32api.Sleep(150)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def mouse_pos(self, cord): # cord tuple
        win32api.SetCursorPos((cord[0], cord[1]))

    def get_cords():  #вывод координат в консоль
        x,y = win32api.GetCursorPos()
        print (x,y)