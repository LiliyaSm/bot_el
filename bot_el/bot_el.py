from PIL import ImageGrab
from PIL import Image, ImageEnhance
import PIL
import cv2
import image_slicer
import pytesseract #C:\Program Files\Tesseract-OCR
import os
import time
import numpy as np
from ctypes import windll # решение проблемы с расширением экрана
import win32api, win32con
import random
import logging

#решение проблемы с расширением экрана
user32 = windll.user32
user32.SetProcessDPIAware()


def screenGrab():
    im = ImageGrab.grab()
    im_my = im.save(os.getcwd() + '\\overall.png', 'PNG') 


    box0 = (1660, 1013, 1910, 1063)
    im = ImageGrab.grab(box0)
    im_my = im.save(os.getcwd() + '\\my.png', 'PNG') 

    box = (435, 644, 479, 669) #box = (431, 629, 486, 682) 
    im = ImageGrab.grab(box)
    im_question = im.save(os.getcwd() + '\\question_small.png', 'PNG') #


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.5)
    #print ('left Down')

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print ("Click.")          #completely optional. But nice for debugging purposes.

def mouse_pos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

#вывод координат в консоль

def get_cords():
    x,y = win32api.GetCursorPos()
    print (x,y)

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

def factory():
    im = ImageGrab.grab()
    im_my = im.save(os.getcwd() + '\\factory.png', 'PNG')



def is_last(): 
    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread("my.png")
    sample_end = cv2.imread("sample\\friends_end.png")
    result1 = cv2.matchTemplate(sample_end, large_image, method)

    if (result1[0][0] < 0.1):
        mouse_pos((1315, 303)) #1025, 1785
        time.sleep(2)
        left_click()
        time.sleep(2)
        mouse_pos((126, 1053))
        time.sleep(2)
        left_click()
        return True

def open_chest():
    #location on the chest
    mouse_pos((460, 750))
    time.sleep(.5)
    left_click()
    time.sleep(.1)


def change_friend(i):
    j = i*70
    position = (210+i*75, 1030) # delta = i*70 1st friend, overall = 15
    print(position)
    mouse_pos(position)
    time.sleep(1)
    left_click()
    n = random.randint(3,5) 
    time.sleep(n)

def crop_img(img):

    #crop_img = img[0:20, 2:14] # hours 12
    #cv2.imwrite("0.png", crop_img)
    #hours = checkPotato("0.png")


    crop_img1 = img[0:20, 33:45] # minutes десятки
    cv2.imwrite("1.png", crop_img1)
    minutes0 = checkPotato("1.png")


    #crop_img2 = img[0:20, 44:56] # minutes единицы

    #cv2.imwrite("2.png", crop_img2)
    #minutes1 = checkPotato("2.png")


    #cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)


def check_question(tile):

    method = cv2.TM_SQDIFF_NORMED
    large_image = cv2.imread(tile)
    sampleIMG = cv2.imread("sample\\question_sample.png")
    method = cv2.TM_SQDIFF_NORMED    
    result = cv2.matchTemplate(sampleIMG, large_image, method)
    print(result[0][0])

    if (result[0][0] < 0.05):
        print("OK")
        return True
    return False


def main():
    i = 0
    time.sleep(7)
    screenGrab()
    while(True):        
        if is_last():
            i = 0
        change_friend(i)
        screenGrab() #creates "question_small.png" and my.png        print(i)   

        if is_mine():
            print("My")
            if check_question("question_small.png"):
                open_chest()


            if i<14:
                change_friend(i+4)
                i=i+1
            elif i>=14:
                mouse_pos((1532, 1025))
                time.sleep(.5)
                left_click()
                time.sleep(3) #loading next friends
                
                change_friend(i-11)
                time.sleep(.5)
                if check_question("question_small.png"):
                    open_chest()

                mouse_pos((500,810)) #сбор палочек
                time.sleep(.5)
                temp = i - 13
                i = temp

                factory()


                change_friend(i)
        print(i)

        if check_question("question_small.png"):
            open_chest()

        mouse_pos((500,810)) #сбор палочек
        time.sleep(.5)
  
        if i < 20:
            i = i+1
        else:
            i = 0
            mouse_pos((1785, 1025))
            time.sleep(.5)
            left_click()
            time.sleep(3) #loading next friends
        

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

