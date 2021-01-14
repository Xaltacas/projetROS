import cv2
from prm import PRM
from pathfinding import smooth


im = cv2.imread("5-final.jpg",cv2.IMREAD_GRAYSCALE)

smoothing = 10
iter = 3

prm = PRM(im,100,10)

lpath = prm.path((74,769),(215,157))



image = prm.returnLinkedMap()

path = image.copy()
path = cv2.cvtColor(path,cv2.COLOR_GRAY2RGB)

miniPath = lpath
for i in range(iter):
    #print("iter = " + str(i))
    miniPath = smooth(miniPath,prm.map,smoothing)


for i in range(len(lpath)-1):
    p1 = lpath[i]
    p2 = lpath[i+1]

    cv2.line(path,(p1[1],p1[0]),(p2[1],p2[0]),(0,0,255),7)

for i in range(len(miniPath)-1):
    p1 = miniPath[i]
    p2 = miniPath[i+1]

    cv2.line(path,(p1[1],p1[0]),(p2[1],p2[0]),(255,0,0),3)

cv2.imwrite("PRM_path_smooth.jpg",path)

print("Ca passe")
