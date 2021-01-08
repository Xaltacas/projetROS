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
                cellules[i,j] = "s" #Sol
            else :
                cellules[i,j] = "o" #Objet
    
    graph = []
    
    for y in range(nb_cellules_Y) :
        for x in range(nb_cellules_X) :
            
            compt = 0
            
            if (x!=0) :#Case de gauche 
                if (cellules[x-1,y] == "s"):                     
                    graph[compt].append(compt-1) 
            
            if(x!=nb_cellules_X - 1) : #Case de droite
                if (cellules[x+1,y] == "s"): 
                    graph[compt].append(compt+1)
            
            if (y!=0) : #Case d'en dessous
                if (cellules[x,y+1] == "s"): #Case d'en dessous                
                    graph[compt].append(compt+width)
            
            if(y!=nb_cellules_X - 1) #Case d'au dessus
                if (cellules[x,y-1] == "s"): #Case d'au dessus                
                    graph[compt].append(compt-width) 
             
            compt++
            
    return graph;
            

def convertir_position_cellule(map,height, width, nb_cellules_X, nb_cellules_Y, posX, posY): 
    
    res = (posX//(width/nb_cellules_X))+nb_cellules_X*(posY//(height/nb_cellules_Y))
    
    return res
              
            
def find_shortest_path(graph, start, end):


        dist = {start: [start]}
        
        q = deque(start)
        
        while len(q):
            at = q.popleft()
            
            for next in graph[at]:
                if next not in dist:
                    dist[next] = [dist[at], next]
                    q.append(next)
            
        return dist.get(end)
                
                
def pathfind_dca(map,height, width, nb_cellules_X, nb_cellules_Y, pos_depart, pos_arrivee) :

    graph = dca(map,height, width, nb_cellules_X, nb_cellules_Y)
    start = convertir_position_cellule(pos_depart)
    end = convertir_position_cellule(pos_arrivee)
    path = find_shortest_path(graph, start, end)
    
    return path
    


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





