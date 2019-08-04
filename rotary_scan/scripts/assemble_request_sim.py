#!/usr/bin/env python
import roslib;roslib.load_manifest('laser_assembler')
import rospy
from sensor_msgs.msg import PointCloud2
from laser_assembler.srv import *

rospy.init_node("cloud_assembler_service_client_node")
rospy.wait_for_service('assemble_scans2')
pub=rospy.Publisher('assembled_cloud',PointCloud2,queue_size=20)
rate=rospy.Rate(50)


#Play bag for pre

while not rospy.is_shutdown():
	try:
		t=rospy.get_rostime()
		print t
		if t.secs==1564392443:
			assemble_scans=rospy.ServiceProxy('assemble_scans2',AssembleScans2)
			resp=assemble_scans(rospy.Time(0,0),t)		
		#print "Row_step %u \t" % resp.cloud.row_step
			pub.publish(resp.cloud)
			print t.secs,t.nsecs
			break

	except Exception,e:
		print "Failed %s" % e
	rate.sleep()

