import numpy as np
import math
import cv2
from bresenham import collide

class Point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toDouble(self):
        return (self.x,self.y)

class Node:
    node_id = None
    point = None


    def __init__(self, x, y, node_id):
        self.point = Point(x,y)
        self.node_id = node_id
        self.neighbors = []

class PRM:


    nodes = []

    def __init__(self, map, numNodes, maxNeighbors = 10):

        self.map = map
        self.x_max = map.shape[0]
        self.y_max = map.shape[1]
        self.x_min = 0
        self.y_min = 0
        self.nbNode = 0
        self.maxNeighbors = maxNeighbors

        self.generateRandomPoints(numNodes)
        self.computeNeighborGraph()

    def add_point(self,x,y):
        p = Node(x,y,self.nbNode)

        if (not collide(p.point.toDouble(), p.point.toDouble(), self.map) and self.isWithinWorld(p.point)):
            self.nodes.append(p)
            self.nbNode += 1
            return self.nbNode-1

        return -1

    def generateRandomPoints(self,nb):
        total = 0
        while(total < nb):
            p = Node(np.random.choice(self.x_max-self.x_min) + self.x_min,
                     np.random.choice(self.y_max-self.y_min) + self.y_min,
                     self.nbNode)

            if (not collide(p.point.toDouble(), p.point.toDouble(), self.map) and self.isWithinWorld(p.point)):
                #print("node ["+str(self.nbNode)+"] : (" + str(p.point.x) + "," + str(p.point.y) + ") added")
                self.nodes.append(p)
                self.nbNode +=1
                total +=1

    def computeNeighborGraph(self):
        for i in self.nodes:
            distanceMap = []
            for j in self.nodes:
                if (i.node_id != j.node_id and not collide(i.point.toDouble(), j.point.toDouble(), self.map)):
                    distanceMap.append((self.getEuclideanDistance(i.point,j.point),j))
                #elif (i.node_id != j.node_id):
                #    print("collide between node ["+str(i.node_id)+"] and ["+str(j.node_id)+"]")

            distanceMap = sorted(distanceMap, key=lambda x: x[0])
            for pair in distanceMap:
                if (len(i.neighbors) >=self.maxNeighbors):
                    break
                #print("node ["+str(i.node_id)+"] and ["+str(pair[1].node_id)+"] linked")
                i.neighbors.append(pair[1])
                pair[1].neighbors.append(i)

    def computeNeighborGraphID(self,  ID):
        i = self.getById(ID)
        distanceMap = []
        for j in self.nodes:
            if (i.node_id != j.node_id and not collide(i.point.toDouble(), j.point.toDouble(), self.map)):
                distanceMap.append((self.getEuclideanDistance(i.point,j.point),j))
            #elif (i.node_id != j.node_id):
            #    print("collide between node ["+str(i.node_id)+"] and ["+str(j.node_id)+"]")

        distanceMap = sorted(distanceMap, key=lambda x: x[0])
        for pair in distanceMap:
            if (len(i.neighbors) >=self.maxNeighbors):
                break
            #print("node ["+str(i.node_id)+"] and ["+str(pair[1].node_id)+"] linked")
            i.neighbors.append(pair[1])
            pair[1].neighbors.append(i)

    def returnLinkedMap(self):
        image = self.map.copy()
        for i in self.nodes:
            for j in i.neighbors:
                cv2.line(image,(i.point.y,i.point.x),(j.point.y,j.point.x),125,1)
        return image

    def path(self,p1,p2):

        end = self.add_point(p2[0],p2[1])
        if(end ==-1):
            print("mauvais end")
            return -1
        else:
            self.computeNeighborGraphID(end)

        start = self.add_point(p1[0],p1[1])
        if(start ==-1):
            print("mauvais start")
            return -1
        else:
            self.computeNeighborGraphID(start)




        dist = [10000.0]*(self.nbNode)
        vset = [True]*(self.nbNode)
        prev = [-1]*(self.nbNode)

        dist[start] = 0

        while True:
            if (sum(vset) == 0):
                break

            low = 10000.0
            u = -1
            for i in xrange(self.nbNode):
                if (vset[i]):
                    if (u == -1 or dist[i] < low):
                        low = dist[i]
                        u = i

            vset[u] = False;

            for v in self.getById(u).neighbors:

                alt = dist[u] + self.getEuclideanDistance(self.getById(u).point, v.point)

                if (alt < dist[v.node_id]):
                    dist[v.node_id] =  alt
                    prev[v.node_id] = u

        print(prev)

        node = end
        path = []
        while True:
            if (node == -1):
                break
            path.append(node)
            node = prev[node]

        #print path
        return path

    def getEuclideanDistance(self,p1, p2):
        return math.sqrt(math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2))

    def isWithinWorld(self,p):
        return (p.x > self.x_min and p.x < self.x_max and p.y > self.y_min and p.y < self.y_max)

    def getNodes(self):
        return self.nodes;

    def getById(self,node_id):
        for i in self.nodes:
            if i.node_id == node_id:
                return i
