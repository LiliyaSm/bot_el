import win32com.client
import win32api, win32con


win32api.Sleep(5000)
shell = win32com.client.Dispatch('WScript.Shell')
shell.SendKeys('{F5}')

