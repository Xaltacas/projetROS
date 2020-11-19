#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math
import time
import numpy as np
import keyboard


x = 0
y = 0
z = 0
theta = 0


if __name__ == "__main__":

    rospy.init_node("teleop_controller")

    cmd_vel_topic = "/cmd_vel"
    velocity_publisher = rospy.Publisher(cmd_vel_topic,Twist,queue_size =10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        v_msg = Twist()
        v_msg.linear.x = 0
        v_msg.linear.y = 0
        v_msg.linear.z = 0
        v_msg.angular.x = 0
        v_msg.angular.y = 0
        v_msg.angular.z = 0
        if keyboard.is_pressed('z'):
            v_msg.linear.x = v_msg.linear.x + 1
        if keyboard.is_pressed('s'):
            v_msg.linear.x = v_msg.linear.x - 1
        if keyboard.is_pressed('q'):
            v_msg.angular.z = v_msg.angular.z + 1
        if keyboard.is_pressed('d'):
            v_msg.angular.z = v_msg.angular.z - 1

        print("loop")
        velocity_publisher.publish(v_msg)

        rate.sleep()
