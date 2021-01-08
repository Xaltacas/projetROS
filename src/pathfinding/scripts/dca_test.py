import cv2
from dca import *


im = cv2.imread("5-final.jpg",cv2.IMREAD_GRAYSCALE)


height,width = im.shape

graphe = dca(im,height, width, width//20, height//20)
cellule_depart = convertir_position_cellule(im,height, width, width//20, height//20, 74, 769)
cellule_arrivee = convertir_position_cellule(im,height, width, width//20, height//20, 215, 157)

path = find_shortest_path(graphe,cellule_depart,cellule_arrivee)

print(path)

"""
image = prm.returnLinkedMap()

cv2.imwrite("PRM.jpg",image)

path = image.copy()
path = cv2.cvtColor(path,cv2.COLOR_GRAY2RGB)


for i in range(len(node_path)-1):
    p1 = prm.getById(node_path[i]).point
    p2 = prm.getById(node_path[i+1]).point

    cv2.line(path,(p1.y,p1.x),(p2.y,p2.x),(0,0,255),3)

cv2.imwrite("PRM_path.jpg",path)

print("Ca passe")
"""
