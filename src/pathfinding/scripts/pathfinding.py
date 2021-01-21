#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

from nav_msgs.srv import GetMap
import math
import time
import numpy as np
import cv2
import prm as algo
from bresenham import collide
from utils import *
from commande import *
import tf

pointList =[]

nextpoint = [0,0,0,0,0,0]
atteint = False

def cb_newGoal(goalMessage):
	global nextpoint
	global atteint

	goalMessage = goalMessage.pose

	rot = quaternion_to_euler(goalMessage.orientation.x,goalMessage.orientation.y,goalMessage.orientation.z,goalMessage.orientation.w)
	nextpoint = [goalMessage.position.x,goalMessage.position.y,goalMessage.position.z,0,0,rot[0]*math.pi/180]

	atteint = False

def generateMap(data):
    xmin, xmax, ymin , ymax = getAOI(data)

    print("AOI",xmin, xmax, ymin , ymax)

    cropped = data[xmin:xmax,ymin:ymax]

    height,width = cropped.shape
    for x in range(height):
        for y in range(width):
            if cropped[x][y] == -1:
                cropped[x][y] = 255
            elif cropped[x][y] == 0:
                cropped[x][y] = 0
            else:
                cropped[x][y] = 255
    img = np.array(cropped,'uint8')



    kernel = np.ones((8,8),'uint8')
    img = cv2.dilate(img,kernel)

    img = cv2.erode(img,kernel)

    img = cv2.medianBlur(np.float32(img),5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
    final = cv2.dilate(img,kernel)

    return 255-final




if __name__ == "__main__":

	rospy.init_node("teleop_from_rviz")

	goal_topic = "/move_base_simple/goal"
	goal_subscriber = rospy.Subscriber(goal_topic,PoseStamped,cb_newGoal) 

	cmd_vel_topic = "/cmd_vel"
	velocity_publisher = rospy.Publisher(cmd_vel_topic,Twist,queue_size =10)

	listener = tf.TransformListener()

	rospy.wait_for_service("dynamic_map")
	service = rospy.ServiceProxy("dynamic_map",GetMap)
	map = service().map
	vect = np.array(map.data)
	data = np.reshape(vect,(1600,1600))

	map = generateMap(data)

	prm = algo.PRM(map,100,10)

	(trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
	rot_angle = quaternion_to_euler(rot[0],rot[1],rot[2],rot[3])

	nextpoint = [trans[0],trans[1],trans[2],0,0,rot_angle[0]*math.pi/180]

	rate = rospy.Rate(10)
	# loop forever until roscore or this node is down
	while not rospy.is_shutdown():
		try:
			# listen to transform
			(trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
			rot_angle = quaternion_to_euler(rot[0],rot[1],rot[2],rot[3])

			currpos = [trans[0],trans[1],trans[2],0,0,rot_angle[0]*math.pi/180]

		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			print("ca merde")
			continue
		# sleep to control the node frequency
		
		

		if(not atteint):

			print("currpos :")
			print(currpos)
			print("nextpoint :")
			print(nextpoint)


			u , w = commande(currpos,nextpoint)

			print("u : {}, w: {}".format(u,w))

			v_msg = Twist()
			v_msg.linear.x = max(min(u,5),-5)
			v_msg.linear.y = 0
			v_msg.linear.z = 0
			v_msg.angular.x = 0
			v_msg.angular.y = 0
			v_msg.angular.z = max(min(-w,1),-1)

			velocity_publisher.publish(v_msg)

			if( math.sqrt((currpos[0] - nextpoint[0]) * (currpos[0] - nextpoint[0]) + (currpos[1] - nextpoint[1]) *(currpos[1] - nextpoint[1])) < 0.1):
				atteint = True
				print("atteint !!")

		rate.sleep()

		

	"""
	miniPath = prm.path((74,769),(215,157))
	#print("minipath : \n")
	#print(miniPath)

	#print("smoothmini")
	#print(smooth(miniPath,4))

	origin = (map.info.origin.position.x,map.info.origin.position.y)
	resolution = map.info.resolution

	globalPathPix = []
	globalPathPos = []
	for elem in miniPath:
		gElem = mini2global(elem,xmin, xmax, ymin , ymax)
		globalPathPix.append(gElem)
		globalPathPos.append(pix2m(gElem,origin,resolution))


	print("global")
	print(globalPathPix)
	print("pos")
	print(globalPathPos)
	"""

