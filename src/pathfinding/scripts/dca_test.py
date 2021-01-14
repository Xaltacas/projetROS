import cv2
from dca import *



im = cv2.imread("5-final.jpg",cv2.IMREAD_GRAYSCALE)


height,width = im.shape

#print(convertir_position_cellule(101, 101, 10, 10, 100, 100))

lpath = pathfind_dca(im,width, height,  width//10, height//10, (74,769),(215,157))

miniPath = smooth(lpath,im,15)
miniPath = smooth(miniPath,im,15)
miniPath = smooth(miniPath,im,15)

#cv2.imwrite("PRM.jpg",image)

path = im.copy()
path = cv2.cvtColor(path,cv2.COLOR_GRAY2RGB)


for i in range(len(lpath)-1):
    p1 = lpath[i]
    p2 = lpath[i+1]

    cv2.line(path,(p1[1],p1[0]),(p2[1],p2[0]),(0,0,255),7)

for i in range(len(miniPath)-1):
    p1 = miniPath[i]
    p2 = miniPath[i+1]

    cv2.line(path,(p1[1],p1[0]),(p2[1],p2[0]),(255,0,0),3)

cv2.imwrite("DCA_path_smooth.jpg",path)

print("Ca passe")


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
