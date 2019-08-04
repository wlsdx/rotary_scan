#!/usr/bin/env python
import serial,sys,time,rospy
import geometry_msgs.msg
import tf2_ros.transform_broadcaster
import math
import tf


if __name__=='__main__':
	rospy.init_node("py_serial_and_tf_broadcaster")
	print 'Starting'
	sio=serial.Serial("/dev/ttyUSB0",9600,8,timeout=5)
	sio.write('1IE\r\n')
	IE0=int(sio.readline()[4:13],16)#Position, string format: '1IE=xxxxxxxx{4D' in hex
	coef=2*math.pi/20000
#tf
	m=tf.TransformBroadcaster()
	t=geometry_msgs.msg.TransformStamped()
	t.header.frame_id='base_link'#The reference frame in this tf msg
	t.child_frame_id='laser'
	
	rate=rospy.Rate(50)#f=50Hz
	
	sio.write("STD\r\nDL1\r\nDI1\r\nAC46.426\r\nDE46.426\r\nVE0.0756\r\nSH1L\r\n")#Movement Start
	try:
		while not rospy.is_shutdown():
			t.header.stamp=rospy.get_rostime()
			sio.write('1IE\r\n')
			IE=int(sio.readline()[4:13],16)-IE0
			theta=IE*coef
			#rotate only around y axis
			t.transform.rotation.w=math.cos(theta)
			t.transform.rotation.y=math.sin(theta)
			m.sendTransformMessage(t)
			print 'Sending'
			rate.sleep()
			if IE>20000:
				rospy.set_param('/scan_over',True)
				sio.write('STD\r\n')#Stop motor
				break
	except Exception,e:
		print "Failed %s" % e		
	finally:
		sio.write('STD\r\n')
