#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import math
import time
import numpy as np
import keyboard


cx = 0
cz = 0

def joyCallBack(joy_message):
    global cx, cz

    cx = joy_message.axes[1]
    cz = joy_message.axes[3]


if __name__ == "__main__":

    rospy.init_node("teleop_joy_bridge")

    joy_topic = "/joy"
    joy_subscriber = rospy.Subscriber(joy_topic,Joy,joyCallBack)


    cmd_vel_topic = "/cmd_vel"
    velocity_publisher = rospy.Publisher(cmd_vel_topic,Twist,queue_size =10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        v_msg = Twist()
        v_msg.linear.x = cx
        v_msg.linear.y = 0
        v_msg.linear.z = 0
        v_msg.angular.x = 0
        v_msg.angular.y = 0
        v_msg.angular.z = cz

        velocity_publisher.publish(v_msg)

        rate.sleep()
