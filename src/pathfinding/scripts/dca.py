import cv2
import numpy as np

class DCA : 
    def __init__(self, map, nb_cellules_X, nb_cellules_Y):

        self.map = map
        self.width = map.shape[0]
        self.height = map.shape[1]
        self.nb_cellules_X = nb_cellules_X
        self.nb_cellules_Y = nb_cellules_Y
        self.deltaX = int(float(self.width)/self.nb_cellules_X)
        self.deltaY = int(float(self.height)/self.nb_cellules_Y)

    def dca(self):
    
        
	
        cellules = [[0 for i in range(self.nb_cellules_X)] for j in range(self.nb_cellules_Y)]
    
        compteur = 0
        for j in range(self.nb_cellules_Y):
            for i in range(self.nb_cellules_X):
                cellule = map[i*self.deltaX:(i+1)*self.deltaX,j*self.deltaY:(j+1)*self.deltaY]
                
                for ligne in cellule :
                    for pixel in ligne :
                        if (pixel == 0) :
                            bol = False
                        
                if (bol) :
                        cellules[j][i] = "s" #Sol
                else :
                    cellules[j][i] = "o" #Objet
                    compteur += 1
                bol=True           
        graph = [[] for i in range(self.nb_cellules_X*self.nb_cellules_Y)]
    
        compt = 0
    
        for y in range(self.nb_cellules_Y) :
            for x in range(self.nb_cellules_X) :
                
                if (cellules[y][x] == "s"):
                
                    if (x!=0) :#Case de gauche 
                        if (cellules[y][x-1] == "s"):                     
                            graph[compt].append(compt-1) 
                    
                    if(x!=nb_cellules_X - 1) : #Case de droite
                        if (cellules[y][x+1] == "s"): 
                            graph[compt].append(compt+1)
                
                    if (y!=0) : #Case d'au dessus
                        if (cellules[y-1][x] == "s"): #Case d'en dessous                
                            graph[compt].append(compt-self.nb_cellules_X)
                
                    if(y!=nb_cellules_Y - 1): #Case d'en dessous
                        if (cellules[y+1][x] == "s"): #Case d'au dessus                
                            graph[compt].append(compt+self.nb_cellules_X)
                 
                compt += 1
                
            return graph;
                
    
    def convertir_position_cellule(self, posX, posY):
            
        height = float(self.height)
        width = float(self.width)
        res = (posX//(width/self.nb_cellules_X))+self.nb_cellules_X*(posY//(height/self.nb_cellules_Y))
        #print(res)
        return int(res)
    
    def convertir_num_cell_milieu_cell(self,num_cellule) :
    
        
        num_x = num_cellule%self.nb_cellules_X
        
        num_y = num_cellule//self.nb_cellules_X
        x = num_x * self.deltaX + self.deltaX/2
        y = num_y * self.deltaY + self.deltaY/2
        return(int(x),int(y))
        
        


                
    def path(self, pos_depart, pos_arrivee) :
    
        
        graph = dca(self)
        start = convertir_position_cellule(self, pos_depart[0], pos_depart[1])
        end = convertir_position_cellule(self, pos_arrivee[0], pos_arrivee[1])
        res = pathfind_dca(self, start, end)
    
        return res
    

    def pathfind_dca(self, start, end):
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
                    
                        alt = dist[u] + self.deltaX
                        
                    else :
                        
                        alt = dist[u] + self.deltaY
    
                    if (alt < dist[v]):
                        dist[v] =  alt
                        prev[v] = u
    
            #print(prev)
    
            cellule = end
            path = []
            while True:
                if (cellule == -1):
                    break
                path.append(cellule)
                cellule = prev[cellule]
    
            #print(path)
        
        
            for k in range (len(path)) :
                path[k] = convertir_num_cell_milieu_cell(self,path[k])
            
            
            return path
        
def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end

    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


    def collide(p1,p2,map):
        for point in get_line(p1,p2):
            x,y = point
            if(map[x,y] == 0):
                #print("collision en {} , {}".format(x,y))
                return True
        return False
            
def smooth(path, map, div = 10):
    _div = 1./div
    subpath= [path[0]]
    prevpoint = path[0]
    for point in path[1:]:
        for i in range(1,div+1):
            diffx = point[0] - prevpoint[0]
            diffy = point[1] - prevpoint[1]

            subpath.append((int(prevpoint[0]+ diffx*i*_div),int(prevpoint[1]+ diffy*i*_div)))
        prevpoint = point

    res = [subpath[0]]
    current = 0
    point = 1
    while True :
        if(point == len(subpath)-1):
            res.append(subpath[point])
            break
        if (collide(subpath[current],subpath[point],map)):
            res.append(subpath[point-1])
            current= point - 1
        point += 1

    return res

"""     
def pathfind_dca(map,height, width, nb_cellules_X, nb_cellules_Y, pos_depart, pos_arrivee) :

    graph = dca(map,height, width, nb_cellules_X, nb_cellules_Y)
    start = convertir_position_cellule(pos_depart)
    end = convertir_position_cellule(pos_arrivee)
    path = find_shortest_path(graph, start, end)
    
    return path

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



