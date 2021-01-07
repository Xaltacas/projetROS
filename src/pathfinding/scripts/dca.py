import cv2
def dca(map,height, width, nb_cellules_X, nb_cellules_Y):

    centres_cellules = []
    deltaX = width//nb_cellules_X
    deltaY = height//nb_cellules_Y
    
    for i in range(nb_cellules_X):
        for j in range(nb_cellules_Y):
            cellule = map[i*deltaX:(i+1)*deltaX,j*deltaY:(j+1)*deltaY]
            for pixel in cellule :
                if (pixel == 0)
                    bol = False
                    
            if (bol) :
                centres_cellules[i,j] = "s" #Sol
            else :
                centres_cellules[i,j] = "o" #Objet
    
    graph = {}
    
    for x in range(nb_cellules_X) :
        for y in range(nb_cellules_Y) :
            if (x==0 && y==0):
            
            elif (x==0 && y==nb_cellules_Y-1):
            
            elif (x==nb_cellules_X-1 && y==0):
            
            elif (x==nb_cellules_X-1 && y==nb_cellules_Y-1):
            
            else :
                
    


"""
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
            res.append(((i(1,1)+i(2,1))/2,(i(1,2)+i(2,2))/2,"s"))
	    elif i(3) == "o" :
            res.append(((i(1,1)+i(2,1))/2,(i(1,2)+i(2,2))/2,"s"))
    return res
"""





