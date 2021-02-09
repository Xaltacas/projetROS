import numpy as np
from bresenham import collide

def getAOI(data):
    height,width = data.shape

    xmin = height
    xmax = 0

    ymin = width
    ymax = 0

    for x in range(height):
        for y in range(width):
            if( data[x][y] != -1):
                xmin = min(xmin,x)
                xmax = max(xmax,x)
                ymin = min(ymin,y)
                ymax = max(ymax,y)

    return xmin, xmax, ymin , ymax

def mini2global(pos,xmin, xmax, ymin , ymax):
    return pos[0] + xmin, pos[1] +ymin

def mini2globalList(path,xmin, xmax, ymin , ymax):
    res = []
    for pos in path:
        res.append((pos[0] + xmin, pos[1] +ymin))

    return res

def reverse(list):
    res = []
    for item in list:
        res = [item] + res

    return res


def global2mini(pos,xmin, xmax, ymin , ymax):
    if( pos[0]>xmax or pos[0]<xmin or pos[1]>ymax or pos[0]<ymin ):
        return None
    return pos[0] - xmin, pos[1] -ymin

def pix2m(pos,origin,resolution):
    return origin[0] + (resolution * pos[0]), origin[1] + (resolution * pos[1])

def pix2mlist(path,origin,resolution):
    res = []
    for pos in path:
	res.append((origin[0] + (resolution * pos[0]), origin[1] + (resolution * pos[1])))
    return res

def m2pix(pos,origin,resolution):
    return int((pos[0] - origin[0])/resolution), int((pos[1] - origin[1])/resolution)

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

    subpath= [res[0]]
    prevpoint = res[0]

    '''
    for point in res[1:]:
        for i in range(1,div+1):
            diffx = point[0] - prevpoint[0]
            diffy = point[1] - prevpoint[1]

            subpath.append((int(prevpoint[0]+ diffx*i*_div),int(prevpoint[1]+ diffy*i*_div)))
        prevpoint = point
    '''
    return res


def quaternion_to_euler(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2>+1.0,+1.0,t2)
    #t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2<-1.0, -1.0, t2)
    #t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return X, Y, Z
