import cv2
import numpy as np
def dca(map,deltaX, deltaY, nb_cellules_X, nb_cellules_Y):

    cellules = [[0 for i in range(nb_cellules_X)] for j in range(nb_cellules_Y)]
    print(len(cellules[0]), len(cellules))
    
    for j in range(nb_cellules_Y):
        for i in range(nb_cellules_X):
            cellule = map[i*deltaX:(i+1)*deltaX,j*deltaY:(j+1)*deltaY]
            
            for ligne in cellule :
                for pixel in ligne :
                    if (pixel == 0) :
                        bol = False
                    
            if (bol) :
                cellules[j][i] = "s" #Sol
            else :
                cellules[j][i] = "o" #Objet
            bol=True
                
    graph = [[] for i in range(nb_cellules_X*nb_cellules_Y)]
    
    compt = 0
    
    for y in range(nb_cellules_Y) :
        for x in range(nb_cellules_X) :
            
            if (cellules[y][x] == "s"):
            
                if (x!=0) :#Case de gauche 
                    if (cellules[y][x-1] == "s"):                     
                        graph[compt].append(compt-1) 
            
                if(x!=nb_cellules_X - 1) : #Case de droite
                    if (cellules[y][x+1] == "s"): 
                        graph[compt].append(compt+1)
            
                if (y!=0) : #Case d'au dessus
                    if (cellules[y-1][x] == "s"): #Case d'en dessous                
                        graph[compt].append(compt-width)
            
                if(y!=nb_cellules_Y - 1): #Case d'en dessous
                    if (cellules[y+1][x] == "s"): #Case d'au dessus                
                        graph[compt].append(compt+width) 
             
            compt += 1
            
    return graph;
            

def convertir_position_cellule(map,height, width, nb_cellules_X, nb_cellules_Y, posX, posY): 
    
    res = (posX//(width/nb_cellules_X))+nb_cellules_X*(posY//(height/nb_cellules_Y))
    
    return res
              
"""          
def find_shortest_path(graph, start, end):


        dist = {start: [start]}
        
        q = deque(start)
        
        while len(q):
            at = q.popleft()
            
            for next in graph[at]:
                if next not in dist:
                    dist[next] = [dist[at],next]
                    q.append(next)
            
        return dist.get(end)
                
"""

                
def pathfind_dca(map,height, width, nb_cellules_X, nb_cellules_Y, pos_depart, pos_arrivee) :

    deltaX = width/nb_cellules_X
    deltaY = height/nb_cellules_Y
    graph = dca(map,deltaX, deltaY, nb_cellules_X, nb_cellules_Y)
    start = convertir_position_cellule(pos_depart)
    end = convertir_position_cellule(pos_arrivee)
    path = find_shortest_path(graph, start, end)
    
    return path
    

def path(graph,deltaX, deltaY,start,end):
        
        if (graph[start] == [] or graph[end] == []):
        
            print("C'est pas possible")
            return -1
            
        
        nb_cellules = len(graph)
        dist = [10000.0]*(nb_cellules)
        vset = [True]*(nb_cellules)
        prev = [-1]*(nb_cellules)

        dist[start] = 0

        while True:
            if (sum(vset) == 0):
                break

            low = 10000.0
            u = -1
            for i in xrange(nb_cellules):
                if (vset[i]):
                    if (u == -1 or dist[i] < low):
                        low = dist[i]
                        u = i

            vset[u] = False;

            for v in graph[u]:

                if(abs(u-v)==1):
                
                    alt = dist[u] + deltaX
                    
                else :
                     alt = dist[u] + deltaY

                if (alt < dist[v]):
                    dist[v] =  alt
                    prev[v] = u

        #print(prev)

        node = end
        path = []
        while True:
            if (node == -1):
                break
            path.append(self.getById(node).point.toDouble())
            node = prev[node]

        #print path
        return path.reverse()
        
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





