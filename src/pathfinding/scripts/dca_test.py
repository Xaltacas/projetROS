import cv2
import dca
from utils import reverse
from pathfinding import smooth

im = cv2.imread("5-final.jpg",cv2.IMREAD_GRAYSCALE)


height,width = im.shape
print(height,width)

#print(convertir_position_cellule(101, 101, 10, 10, 100, 100))



#lpath = pathfind_dca(im,width, height,  width//10, height//10, (74,769),(215,157))
nb_cellules_X = 100
nb_cellules_Y = 100
algo = dca.DCA(im,nb_cellules_X,nb_cellules_Y)

lpath = algo.path((74,769),(215,157))

miniPath = smooth(lpath,im,15)
miniPath = smooth(miniPath,im,15)
miniPath = smooth(miniPath,im,15)
miniPath = reverse(miniPath)
miniPath = smooth(miniPath,im,15)
miniPath = reverse(miniPath)

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

delta_X = height/nb_cellules_X+1
for i in range(nb_cellules_X):
	p1 = [i*delta_X,0]
	p2 = [i*delta_X,width]

	cv2.line(path,(p1[1],p1[0]),(p2[1],p2[0]),(128,128,128),1)

delta_Y = width/nb_cellules_Y+1
for i in range(nb_cellules_Y):
    p1 = [0,i*delta_Y]
    p2 = [height,i*delta_Y]

    cv2.line(path,(p1[1],p1[0]),(p2[1],p2[0]),(128,128,128),1)

cv2.imwrite("DCA_path_smooth.jpg",path)

print("Ca passe")
