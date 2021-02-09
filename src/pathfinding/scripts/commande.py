import math as m


def commande(pos_rob,point_objectif) :
    dx = point_objectif[0] - pos_rob[0] #distance entre le robot et le point projetee sur x
    dy = point_objectif[1] - pos_rob[1] #distance entre le robot et le point projetee sur y
    dist = m.sqrt(dx**2 + dy**2) #distance euclidienne
    theta = normalize_angle(pos_rob[5])  #angle du robot

    #print(theta)
    beta = m.atan2(dy,dx) #angle du point par rapport au robot
    #print(beta)
    alpha = normalize_angle(beta - theta) #difference d'angle
    #print(alpha)
    beta_suivant = point_objectif[5]
    dbeta = normalize_angle(beta_suivant-beta)

    
    ## Gains ##
    mult = 3	

    Kp = 1/(1+(mult*abs(alpha)))
    Ka = 10
    Kb = -0
    



    u = Kp
    w= Ka*alpha + Kb*dbeta
    
    
    return u ,w
    
    
def normalize_angle(angle) : #Normalise un angle entre -pi et pi

    while(angle > m.pi or angle < -m.pi) :
        if(angle > m.pi) :
            angle -= 2*m.pi  
        elif(angle < -m.pi) :
            angle += 2*m.pi 
    return angle

