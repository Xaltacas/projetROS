import cv2
import numpy as np
#from bresenham import get_line
from utils import smooth
import math
from bresenham import collide

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
		bol=True   
		      
		for j in range(self.nb_cellules_Y):
			for i in range(self.nb_cellules_X):
				cellule = self.map[i*self.deltaX:(i+1)*self.deltaX,j*self.deltaY:(j+1)*self.deltaY]

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

					if(x!=self.nb_cellules_X - 1) : #Case de droite
						if (cellules[y][x+1] == "s"): 
							graph[compt].append(compt+1)

					if (y!=0) : #Case d'au dessus
						if (cellules[y-1][x] == "s"): #Case d'en dessous                
							graph[compt].append(compt-self.nb_cellules_X)

					if(y!=self.nb_cellules_Y - 1): #Case d'en dessous
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
    
        
		self.graph = self.dca()
		print(len(self.graph))
		start = self.convertir_position_cellule(pos_depart[0], pos_depart[1])
		print('start =', start)
		end = self.convertir_position_cellule(pos_arrivee[0], pos_arrivee[1])

		res = self.pathfind_dca(start, end)


		return res
    

    def pathfind_dca(self, start, end):
            if (self.graph[start] == []):
            
                print("C'est pas possible start")
                return -1
                
            elif (self.graph[end] == []):
            
            	print("C'est pas possible end")
                return -1
                  
            nb_cellules = len(self.graph)
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
    
                for v in self.graph[u]:
    
                    if(abs(u-v)==1):
                    
                        alt = dist[u] + self.deltaX
                        
                    else :
                        
                        alt = dist[u] + self.deltaY
    
                    if (alt < dist[v]):
                        dist[v] =  alt
                        prev[v] = u
    
            
    
            cellule = end
            path = []
            

            while True:
                if (cellule == -1):
                    break
                path.append(cellule)
                cellule = prev[cellule]
    
            
        
        
            for k in range (len(path)) :
                path[k] = self.convertir_num_cell_milieu_cell(path[k])
            
            

            return path





