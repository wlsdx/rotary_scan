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
#tf
	m=tf.TransformBroadcaster()
	t=geometry_msgs.msg.TransformStamped()
	t.header.frame_id='base_link'#The reference frame in this tf msg
	t.child_frame_id='laser'
	#t.header.stamp=rospy.Time(0)
	#t.transform.translation.x=1
	theta=0
	dtheta=math.pi/500
	#rotate only around y axis
	t.transform.rotation.w=math.cos(theta)
	t.transform.rotation.y=math.sin(theta)

	rate=rospy.Rate(50)
	while not rospy.is_shutdown():
		t.header.stamp=rospy.get_rostime()
		t.transform.rotation.w=math.cos(theta)
		t.transform.rotation.y=math.sin(theta)
		theta=theta+dtheta
		m.sendTransformMessage(t)
		print 'Sending'
		rate.sleep()
'''	
	rospy.wait_for_service('assemble_scans')
	try:
		assemble_scans=rospy.ServiceProxy('assemble_scans',AssembleScans)
		resp=assemble_scans(rospy.Time(0,0),rospy.get_rostime())
'''

'''
#serial

sio=serial.Serial("/dev/ttyUSB0",9600,8,timeout=250)
sio.write("STD\r\nDL1\r\nDI1\r\nAC100\r\nDE100\r\nVE10\r\nSH1L\r\n")
time.sleep(10)
sio.write("STD\r\n")
print "done"
'''
