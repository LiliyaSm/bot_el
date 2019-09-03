from PIL import ImageGrab
from PIL import Image, ImageEnhance
import PIL
import cv2
#import pytesseract #C:\Program Files\Tesseract-OCR
import os
import time
import numpy as np
from ctypes import windll # решение проблемы с расширением экрана
import win32api, win32con
import random
import logging
from RepeatedTimer import RepeatedTimer
import win32com.client
from find_templ import find_templ
from datetime import datetime

#решение проблемы с расширением экрана
user32 = windll.user32
user32.SetProcessDPIAware()


def screen_grab():
    im = ImageGrab.grab()
    im_my = im.save(os.getcwd() + '\\overall.png', 'PNG') 

    box0 = (1830, 1026, 1905, 1060)
    im = ImageGrab.grab(box0)
    im_my = im.save(os.getcwd() + '\\my.png', 'PNG') 

    box = (435, 644, 479, 669) #box = (431, 629, 486, 682) 
    im = ImageGrab.grab(box)
    im_question = im.save(os.getcwd() + '\\question_small.png', 'PNG') #


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
        #time.sleep(5)
        win32api.Sleep(n)   
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_ABSOLUTE,x,y,0,0)
        win32api.Sleep(400)
        #time.sleep(2)
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

mouse = Mouse()

def mouse_pos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

def reload():
    shell = win32com.client.Dispatch('WScript.Shell')
    shell.SendKeys('{F5}')
    win32api.Sleep(30000)

def tropic_farm(): 
    mouse.left_click(60, 410)
    mouse.drag(1000, 800,460, 400, False) #460, 400

    list = []
    for i in range(460, 960, 100): #x увеличила на 100
        for j in range(400, 900, 100): #y увеличила на 100
            list.append((i,j))
    random.shuffle(list)
    while True:        
        #index = list.index(random.choice(list))
        #print(random.choice(list))
        print(list)
        if list:
            cords = (list.pop())
            mouse.move(cords[0], cords[1])
        else:
            mouse.left_up()
            break

    mouse.left_click(1100, 440)
    mouse.left_click(1100, 540)
    mouse.left_click(1100, 640)

    mouse.left_click(1315, 440)
    mouse.left_click(1315, 540)
    mouse.left_click(1315, 640)

    mouse.left_click(1510, 230)
    



def get_cords():  #вывод координат в консоль
    x,y = win32api.GetCursorPos()
    print (x,y)

def comparison(box, name, path):
    #name - name of large_image
    #path - path to sample "sample\\question_sample.png"
    im = ImageGrab.grab(box).save(os.getcwd() + '\\' + name, "PNG")   
    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread(name)
    sample_IMG = cv2.imread(path)  
    result = cv2.matchTemplate(sample_IMG, large_image, method)
    return result

def is_mine():    
    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread("my.png")
    sample_my = cv2.imread("sample\\my_sample.png") 
    result = cv2.matchTemplate(sample_my, large_image, method)
    #print(result[0][0])
    if (result[0][0] < 0.05):
        print("MY")
        return True
    return False

def check_buttons(buttons):
    for i in range(3):
        result = comparison(buttons[i], "button.png", "sample\\speed_up.png")            
        print(result[0][0])
        if (result[0][0] > 0.1): #if there is no overlap
            mouse.left_click(buttons[i][0], buttons[i][1]) #press the button
            time.sleep(2)

def checking_cafe():
    name = 'checking_cafe.png'
    path = "sample\\question_sample.png"
    box = (1135, 429, 1178, 453)
    result = comparison(box, name, path)
    time.sleep(2)  
    if (result[0][0] < 0.05):        #there is question mark
        mouse.left_click(1250, 565) #open cafe
        print("open cafe")
        time.sleep(.5)
        buttons = [(616, 493, 730, 525), (616, 642, 730, 675), (616, 792, 730, 825)]
        check_buttons(buttons)
        mouse.left_click(1505,210) #close window
        time.sleep(2)
        return True
    return False

def checking_factory():
    name = 'check_factory.png'
    path = "sample\\check_box.png"
    box = (70, 1010, 85, 1025)
    result = comparison(box, name, path)

    if (result[0][0] < 0.05):        #there is green sign
        mouse.left_click(50, 1035) #open factory
        print("open factory")
        time.sleep(.5)
        buttons = [(964, 785, 1077, 816), (1149, 785, 1262, 816), (1337, 785, 1450, 816)]
        check_buttons(buttons)
        mouse.left_click(1505,210) #close window
        time.sleep(2)
        return True
    return False

def check_feeding():
    time.sleep(2)
    mouse.left_click(65, 280) #65, 280
    time.sleep(2)
    buttons = [(853, 748, 963, 779), (1051, 748, 1164, 779), (1245, 748, 1358, 779)]
    check_buttons(buttons)
    mouse.left_click(960, 831) # click in case of level up
    mouse.left_click(1425,205) #close window

def check_missions():
    time.sleep(2)
    name = 'check_missions.png'
    path = "sample\\check_box.png"
    box = (91, 151, 105, 165)
    result = comparison(box, name, path)
    if (result[0][0] < 0.05):        #there is green sign
        time.sleep(2)
        mouse.left_click(69, 177)
        print("open missions")
        time.sleep(.5)
        buttons = [(643, 541), (650, 680), (636, 776)]
        for i in range(3):
            mouse.left_click(buttons[i][0], buttons[i][1])
            name = 'check_missions1.png'
            path = "sample\\check_missions_sample.png"
            box = (1010, 673, 1180, 715)
            result = comparison(box, name, path)
            if (result[0][0] > 0.05):
               mouse.left_click(1050,700) #there is no overlap        
               time.sleep(2)
               mouse.left_click(963,803)

        mouse.left_click(1425,205) #close window

def is_last(): 
    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread("my.png")
    sample_end = cv2.imread("sample\\friends_end.png")
    result1 = cv2.matchTemplate(sample_end, large_image, method)

    if (result1[0][0] < 0.1):
        mouse.left_click(920, 722) # it could be the chest message
        mouse.left_click(1315, 303) #1025, 1785 close friend warning window
        time.sleep(2)
        mouse.left_click(126, 1053)
        time.sleep(2)
        return True


def is_friend(): 
    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread("my.png")
    sample_end = cv2.imread("sample\\is_friend_sample.png")
    result1 = cv2.matchTemplate(sample_end, large_image, method)

    if (result1[0][0] < 0.1):
        return True
    else:
        return False


def change_friend(i):

    position = (210+i*75, 1015) # delta = i*75 1st friend, overall = 15
    mouse.left_click(position[0], position[1])
    n = random.randint(3,6) 
    time.sleep(n)

def crop_img(img):

    crop_img1 = img[0:20, 33:45] # minutes десятки
    cv2.imwrite("1.png", crop_img1)
    minutes0 = checkPotato("1.png")

    #cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)

def change_i(i):
    if i<14:
        change_friend(i+3)
        screen_grab()
        check_question()   
        i=i+1
        return i
    elif i>=14:
        mouse.left_click(1532, 1025)
        time.sleep(3) #loading next friends                
        change_friend(i-11)
        time.sleep(.5)
        screen_grab()
        check_question()
        i = i - 13
        return i
   

def check_question():
    mouse_pos((500,810)) #сбор палочек
    time.sleep(.5)

    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread("question_small.png")
    sampleIMG = cv2.imread("sample\\question_sample.png")
    method = cv2.TM_SQDIFF_NORMED    
    result = cv2.matchTemplate(sampleIMG, large_image, method)
    print(result[0][0])

    if (result[0][0] < 0.05):
        print("OPEN")
        mouse.left_click(460, 750) #open chest
        time.sleep(.5)
    return False

class GameLogic(object):
    def __init__(self):
        self._flag = False
        
    def change_glade(self):
        self._flag = True # its time to check another glade
        print(self._flag)
    
    def run(self):
        rt = RepeatedTimer(5400, self.change_glade) # it auto-starts, no need of rt.start()
        if self._flag:
            print(time.localtime())   
            buttons = [(645, 430) , (840, 425), (1060, 460), (1272, 453)]
            for i in range(4): 
                mouse.left_click(1860, 1035)               
                mouse.left_click(buttons[i][0], buttons[i][1])
                time.sleep(4)
                check_feeding()
                check_missions()
                
            print("checking glade")
            print("sleep")
            time.sleep(300)
            
                
            self._flag = False

game = GameLogic()

def main():
    i = 0
    time.sleep(5)   
 
    while(True):
        screen_grab()  #creates "question_small.png" and my.png        print(i)      

        if is_friend():    
            check_question()
  
            if i < 20:
                i = i+1
            else:
                i = 0
                mouse.left_click(1785, 1025)
                time.sleep(3) #loading next friends

        elif is_mine():

            check_question()
            game.run()
            print("my")            
            tropic_farm()
            checking_factory()
            i = change_i(i)   #  меняю счетчик из-за своей страницы
            print("NEW ", i)
            
        elif is_last():
            i = 0
            
        else:
            reload()
            win32api.Sleep(10000)
            print(str(datetime.now())[0:19] + ' :reload')
            screen_grab()
            f = "overall.png"
            t = "sample/close_button.png"
            t2 = "sample/full_screen.png"

            img = cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            img_tpl = cv2.imread(t,cv2.IMREAD_GRAYSCALE)
            img_tpl1 = cv2.imread(t2, cv2.IMREAD_GRAYSCALE)

            while True:

                screen_grab()
                img = cv2.imread(f,cv2.IMREAD_GRAYSCALE)

                try:
                    coord = find_templ(img, img_tpl)
                    print(coord)
                    print("window is closed")
                    mouse.left_click(coord[0][0], coord[0][1])
                except:
                        break

                win32api.Sleep(4000)


            try:
                coord = find_templ( img, img_tpl1 )
                print(coord)
                print("window is full")
                mouse.left_click(coord[0][0], coord[0][1])
            except:
                pass

            win32api.Sleep(2000)
            i = 3
        change_friend(i) 

if __name__ == '__main__':
    main()






        #method = cv2.TM_SQDIFF_NORMED
    #path = r"C:\Users\lilii\source\repos\bot_el\bot_el\samples"
    ## Read the images from the file
    #samples = [s for s in os.listdir(path)]
    #large_image = cv2.imread(tile)

    #for sample in samples:
    #    #check for number
    #    sampleIMG = cv2.imread("samples\\" + sample)
    #    result = cv2.matchTemplate(sampleIMG, large_image, method)
    #    print(result[0][0])
    #    print(sample)
    #    if (result[0][0] < 0.05):
    #        print(sample)
    #        return sample
    #return False





    
#def checkPotato(tile):

#    im = Image.open(tile)
#    maxsize = (1028, 1028)
#    resized = im.resize(maxsize)

#    contrast_enhancer = ImageEnhance.Contrast(resized)
#    pil_enhanced_image = contrast_enhancer.enhance(4)
#    enhanced_image = np.asarray(pil_enhanced_image) #сделали массив
#    r, g, b = cv2.split(enhanced_image)
#    enhanced_image = cv2.merge([b, g, r])
#    enhanced_image = Image.fromarray(enhanced_image)#сделали изображение
#    enhanced_image.save("2.png_thumbnail.png", "png")
#    gr = Image.open("2.png_thumbnail.png")
#    gray = gr.convert('1')

#    gray = np.asarray(gray, dtype=np.uint8) 
#    print(type(gray))
#    cv2.imshow('gray', gray)
#    #cv2.waitKey()

#    gray.save("2.png_thumbnail.png", "png")

#    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#    text = pytesseract.image_to_string(gray, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

#    print(text)

#    #img = cv2.imread(tile)
#    # if your image is not already grayscale :
#    #img = cv2.cvtcolor(img, cv2.color_bgr2gray)
#    #threshold = 180 # to be determined
#    #img_binarized = cv2.threshold(img, threshold, 255, cv2.thresh_binary)
#    #pil_img = image.fromarray(img_binarized)

