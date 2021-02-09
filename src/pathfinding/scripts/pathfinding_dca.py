#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose

from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker


from nav_msgs.srv import GetMap
import math
import time
import numpy as np
import cv2
import dca as algo
from bresenham import collide
from utils import *
from commande import *
import tf

pointList =[]


robot_pose = [0,0,0,0,0,0]



def cb_newGoal(goalMessage):
	global pointList
	global dca

	goalMessage = goalMessage.pose
	
	print(goalMessage)
	print(robot_pose)

	pixRP = m2pix((robot_pose[1],robot_pose[0]),origin,resolution)
	pixGM = m2pix((goalMessage.position.y,goalMessage.position.x),origin,resolution)


	print(pixRP)
	print(pixGM)


	pixRP = global2mini(pixRP,xmin, xmax, ymin , ymax)
	pixGM = global2mini(pixGM,xmin, xmax, ymin , ymax)

	pixRP = (pixRP[1],pixRP[0])
	pixGM = (pixGM[1],pixGM[0])


	print("position initiale : ",pixRP)
	print("objectif :",pixGM)

	
	lpath = dca.path(pixRP,pixGM) ##### la la liste est inversee

	if(lpath == -1):
		print("echec dca")
		return

	print("lpath prereverse",lpath)

	lpath = reverse(lpath)

	print("lpath post reverse",lpath)

	miniPath = smooth(lpath,dca.map,5)

	print("miniPath",miniPath)
	
	path = mini2globalList(miniPath,xmin, xmax, ymin , ymax)

	

	rpath = pix2mlist(path,origin,resolution)

	pointList = []	

	for k, point in enumerate(rpath[:-1]):
		pointList.append([point[1],point[0],0,0,0,math.atan2(point[0]-rpath[k+1][0],point[1]-rpath[k+1][1])])
	

	rot = quaternion_to_euler(goalMessage.orientation.x,goalMessage.orientation.y,goalMessage.orientation.z,goalMessage.orientation.w)
	nextpoint = [goalMessage.position.x,goalMessage.position.y,0,0,0,rot[0]*math.pi/180]

	pointList.append(nextpoint)

	print(pointList)
	

def generateMap(data):

    global xmin, xmax, ymin , ymax
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

	marker_topic = "/visualization_marker_array"
	marker_publisher = rospy.Publisher(marker_topic,MarkerArray,queue_size =10)

	listener = tf.TransformListener()

	rospy.wait_for_service("dynamic_map")
	service = rospy.ServiceProxy("dynamic_map",GetMap)
	map = service().map

	origin = (map.info.origin.position.x ,map.info.origin.position.y)
	resolution = map.info.resolution 

	vect = np.array(map.data)
	data = np.reshape(vect,(1600,1600))

	global xmin, xmax, ymin , ymax


	map = generateMap(data)

	global dca

	dca = algo.DCA(map,10,10)

	print("dca ready")	

	(trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
	rot_angle = quaternion_to_euler(rot[0],rot[1],rot[2],rot[3])

	robot_pose = [trans[0],trans[1],trans[2],0,0,rot_angle[0]*math.pi/180]

	nextpoint = [trans[0],trans[1],trans[2],0,0,rot_angle[0]*math.pi/180]

	rate = rospy.Rate(10)
	# loop forever until roscore or this node is down
	while not rospy.is_shutdown():
		try:
			# listen to transform
			(trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
			rot_angle = quaternion_to_euler(rot[0],rot[1],rot[2],rot[3])

			robot_pose = [trans[0],trans[1],trans[2],0,0,rot_angle[0]*math.pi/180]

		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			print("ca merde")
			continue
		# sleep to control the node frequency
		
		

		if(len(pointList) > 0):

			#print("robot_pose :")
			#print(robot_pose)
			#print("nextpoint :")
			#print(nextpoint)


			u , w = commande(robot_pose,pointList[0])

			#print("u : {}, w: {}".format(u,w))

			v_msg = Twist()
			v_msg.linear.x = max(min(u,5),-5)
			v_msg.linear.y = 0
			v_msg.linear.z = 0
			v_msg.angular.x = 0
			v_msg.angular.y = 0
			v_msg.angular.z = max(min(w,1),-1)

			velocity_publisher.publish(v_msg)
			dist = math.sqrt((robot_pose[0] - pointList[0][0]) * (robot_pose[0] - pointList[0][0]) + (robot_pose[1] - pointList[0][1]) *(robot_pose[1] - pointList[0][1]))
			#print("dist :",dist)
			if( dist < 0.3):
				pointList.pop(0)
				print("=================================\n\natteint !!\n=================================\n")
				print(pointList)


			mArray = MarkerArray()
			for k, point in enumerate(pointList):
				marker = Marker()
				marker.header.frame_id = "map"
				marker.id = k
				marker.pose.position.x = point[0]
				marker.pose.position.y = point[1]
				marker.pose.position.z = 0
				marker.pose.orientation.x = 0
				marker.pose.orientation.y = 0
				marker.pose.orientation.z = 0
				marker.pose.orientation.w = 1
				marker.scale.x = 0.5
				marker.scale.y = 0.5
				marker.scale.z = 0.5
				marker.color.r = 253/255.
				marker.color.g = 108/255.
				marker.color.b = 158/255.
				marker.color.a = 1

				marker.type = 2

				mArray.markers.append(marker)
			
			marker_publisher.publish(mArray)

					

		rate.sleep()

		

