import math as m


def commande(pos_rob,point_objectif) :
    dx = point_objectif[0] - pos_rob[0] #distance entre le robot et le point projetee sur x
    dy = point_objectif[1]-pos_rob[1] #distance entre le robot et le point projetee sur y
    dist = m.sqrt(dx**2 + dy**2) #distance euclidienne
    theta = pos_rob[5]  #angle du robot
    beta = m.atan2(dy,dx) #angle du point par rapport au robot
    print(beta)
    alpha = beta - theta #difference d'angle
    print(alpha)
    beta_suivant = point_objectif[5]
    dbeta = beta_suivant - beta
    print(dbeta)
    ## Gains ##
    Kp = 1
    Ka = 1
    Kb = 1
    
    
    u = Kp*dist
    w= Ka*alpha + Kb*dbeta
    
    
    
    return u, w
    
    
pos_rob = [-0.2529,-0.5586,0.02,0,0,87.4663]
point_objectif = [-0.32,0.8575,0,0,0,89.1113]

print(commande(pos_rob, point_objectif))
    
    
    
    
