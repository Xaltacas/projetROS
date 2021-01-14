def getAOI(map):
    height,width = map.shape

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

def global2mini(pos,xmin, xmax, ymin , ymax):
    if( pos[0]>xmax or pos[0]<xmin or pos[1]>ymax or pos[0]<ymin ):
        return None
    return pos[0] - xmin, pos[1] -ymin

def pix2m(pos,origin,resolution):
    return origin[0] + (resolution * pos[0]), origin[1] + (resolution * pos[1])

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