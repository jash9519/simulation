#!/usr/bin/env python
"""
Simple example of subscribing to sensor messages and publishing
twist messages to the turtlebot.

Author: Nathan Sprague
Version: 1/12/2015

"""
import rospy
import math

# Twist is the message type for sending movement commands.
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# globals
SCAN = None

# This function will be called every time a new scan message is
# published.
def scan_callback(scan_msg):
	""" scan will be of type LaserScan """

	# Save a global reference to the most recent sensor state so that
	# it can be accessed in the main control loop.
	# (The global keyword prevents the creation of a local variable here.)
	global SCAN
	SCAN = scan_msg

# This is the 'main'
def start():
    
	# Turn this into an official ROS node named approach
	rospy.init_node('approach')

	# Subscribe to the /scan topic.  From now on
	# scan_callback will be called every time a new scan message is
   	# published.
    	rospy.Subscriber('/laser/scan', LaserScan, scan_callback)

   	# Create a publisher object for sending Twist messages to the
    	# turtlebot_node's velocity topic. 
    	bot_motion_pub = rospy.Publisher('/gz/cmd_vel', Twist) 

    	# Create a twist object. 
    	# twist.linear.x represents linear velocity in meters/s.
    	# twist.angular.z represents rotational velocity in radians/s.
    	bot_motion = Twist()

    	# Wait until the first scan is available.
    	while SCAN is None and not rospy.is_shutdown():
        	rospy.sleep(.1)

    	# Rate object used to make the main loop execute at 10hz.
    	rate = rospy.Rate(1) 

    	while not rospy.is_shutdown():
		for i in range(0,9):
			if (SCAN.ranges[i] > 0 and SCAN.ranges[i] < 2):
				if (i >= 5):
					rospy.loginfo("RIGHT")
					bot_motion.angular.z = 1.5
				else:
					rospy.loginfo("LEFT")
					bot_motion.angular.z = -1.5
			elif (SCAN.ranges[i] > 3 and SCAN.ranges[i] < 4):
				if (i >= 5):
					rospy.loginfo("RIGHT")
					bot_motion.angular.z = 1.0
				else:
					rospy.loginfo("LEFT")
					bot_motion.angular.z = -1.0
			else:
				bot_motion.linear.x = -0.2
				bot_motion.angular.z = 0.0
		bot_motion_pub.publish(bot_motion)



        	rate.sleep()           # Pause long enough to maintain correct rate.
        

# This is how we usually call the main method in Python. 
if __name__ == "__main__":
    start()
