import cv2
def dca_recursif(map, x1, y1, x2, y2):
    res = []
    #Terminaison
    if ((x1,y1) == (x2,y2)) :
            if map(x1,y1) == 255:
                res.append(((x1, y1), (x2, y2), "s"))
            elif map(x1,y1) == 0 :
                res.append(((x1, y1), (x2, y2), "o"))


    else :
        pixel_init = map(x1,y1)
        bol = True
        for i in range(x1, x2+1) :
            for j in range(y1, y2+1) :
                if (map(i,j) != pixel_init) :
                    bol = False
                    break
        if bol:
            if map(x1,y1) == 255:
                res.append(((x1, y1), (x2, y2), "s"))
            elif map(x1,y1) == 0 :
                res.append(((x1, y1), (x2, y2), "o"))     
        else :     
            x_inter = (x1 + x2)/2
            y_inter = (y1 + y2)/2
            dca_recursif(map, x1, y1, x_inter, y_inter)
            dca_recursif(map, x_inter, y_inter, x2, y2)

    return res
        
def centre_rectangles_sol(liste) :
    res = []
    for i in liste :
        if i(3) == "s" :
            res.append(((i(1,1)+i(2,1))/2,(i(1,2)+i(2,2))/2))
    return res

map = cv2.imread("home/polytech/projetROS/5-final.jpg",cv2.IMREAD-GRAYSCALE)

height,width = map.shape
res = dca_recursif(map, 0, 0, height, width) 
print(res(1)) 
close()   