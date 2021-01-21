#!/usr/bin/env python
import rospy
import tf
from utils import *

if __name__ == '__main__':
    # initialize node
    rospy.init_node('tf_listener')
    # print in console that the node is running
    rospy.loginfo('started listener node !')
    # create tf listener
    listener = tf.TransformListener()
    # set the node to run 1 time per second (1 hz)
    rate = rospy.Rate(1.0)
    # loop forever until roscore or this node is down
    while not rospy.is_shutdown():
        try:
            # listen to transform
            (trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
            rot_angle = quaternion_to_euler(rot[0],rot[1],rot[2],rot[3])
            # print the transform
            rospy.loginfo('---------')
            rospy.loginfo('Translation: ' + str(trans))
            rospy.loginfo('Rotation: ' + str(rot))
            rospy.loginfo('Rot_angle: ' + str(rot_angle))
            
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        # sleep to control the node frequency
        rate.sleep()