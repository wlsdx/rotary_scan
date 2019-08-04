#!/usr/bin/env python
import serial,sys,time,rospy
import geometry_msgs.msg
import tf2_ros.transform_broadcaster
import math
import tf
#import roslib;roslib.load_manifest('laser_assembler')
#from laser_assembler.srv import *


if __name__=='__main__':
	rospy.init_node("py_serial_and_tf_broadcaster")
	print 'Starting'
	m=tf.TransformBroadcaster()
	t=geometry_msgs.msg.TransformStamped()
	t.header.frame_id='base_link'#The reference frame in this tf msg
	t.child_frame_id='laser'
	#t.header.stamp=rospy.Time(0)
	z=0
	dz=0.002
	#rotate only around y axis
	#t.transform.rotation.w=math.cos(theta)
	#t.transform.rotation.y=math.sin(theta)
	t.transform.rotation.w=1
	rate=rospy.Rate(50)
	print 'Sending'
	while not rospy.is_shutdown():
		t.transform.translation.z=z
		z=z+dz
		t.header.stamp=rospy.get_rostime()
		m.sendTransformMessage(t)
		#print t
		rate.sleep()

