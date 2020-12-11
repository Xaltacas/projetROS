import cv2
from prm import PRM


im = cv2.imread("5-final.jpg",cv2.IMREAD_GRAYSCALE)


prm = PRM(im,100,10)





node_path = prm.path((74,769),(215,157))

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
