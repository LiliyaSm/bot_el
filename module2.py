import sys
import os
import numpy as np
import cv2
from scipy.ndimage import maximum_filter


def find_templ( img, img_tpl ):
    # размер шаблона
    h,w = img_tpl.shape

    # строим карту совпадений с шаблоном
    match_map = cv2.matchTemplate( img, img_tpl, cv2.TM_CCOEFF_NORMED)

    max_match_map = np.max(match_map) # значение карты для области максимально близкой к шаблону
    print(max_match_map)
    if(max_match_map < 0.71): # совпадения не обнаружены 
        return []

    a = 0.7 # коэффициент "похожести", 0 - все, 1 - точное совпадение 

    # отрезаем карту по порогу 
    match_map = (match_map >= max_match_map * a  ) * match_map  

    # выделяем на карте локальные максимумы
    match_map_max = maximum_filter(match_map, size=min(w,h) ) 
    # т.е. области наиболее близкие к шаблону
    match_map = np.where( (match_map==match_map_max), match_map, 0) 

    # координаты локальных максимумов
    ii = np.nonzero(match_map)
    rr = tuple(zip(*ii))

    res = [ [ c[1], c[0], w, h ] for c in rr ]
   
    return res

def main():
  
    f = "after_reload.png"
    t = "sample/close_button.png"
     

    img = cv2.imread(f,cv2.IMREAD_GRAYSCALE)
    img_tpl = cv2.imread(t,cv2.IMREAD_GRAYSCALE)
    coord = find_templ( img, img_tpl )

    #top_left = (c[0],c[1])
    #bottom_right = (c[0] + c[2], c[1] + c[3])

    for c in coord:
        print(c)
    print(len(coord))
    print("- - - - - - - - - - - - - - -" )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == "__main__":
    print("OpenCV ",cv2.__version__)
    sys.exit(main())


