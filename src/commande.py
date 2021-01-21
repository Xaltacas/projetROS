import math as m


def commande(pos_rob,point_objectif) :
    dx = point_objectif[0] - pos_rob[0] #distance entre le robot et le point projetee sur x
    dy = point_objectif[1]-pos_rob[1] #distance entre le robot et le point projetee sur y
    dist = m.sqrt(dx**2 + dy**2) #distance euclidienne
    theta = pos_rob[5]  #angle du robot
    beta = m.atan2(dy,dx) #angle du point par rapport au robot
    alpha = beta - theta #difference d'angle
    beta_suivant = point_objectif[5]
    dbeta = beta_suivant-beta
    
    ## Gains ##
    Kp = 1
    Ka = 1
    Kb = 1
    
    
    u = Kp*dist
    w= Ka*alpha + Kb*dbeta
    
    
    
    res = [u,w]
    
    return res
    
    
    
    
    
