# rotary_scan
用步进电机带动激光雷达转动，在ROS上控制并得到转动扫描的结果  

![structure](/structure.png)

## 一、如何使用rotary_scan
### 软件

1. 安装[ROS kinetic](https://wiki.ros.org/kinetic/Installation) （操作系统建议使用和开发时一致的Ubuntu 16.04）
2. 将rotary_scan文件夹复制到catkin工作空间的src文件夹，编译，例：  
#注意git链接(试一下要不要编译，要不要说明依赖)
	```
	mkdir -p catkin_ws/src
	cd catkin_ws/src
	git clone https://github.com/wlsdx/rotary_scan/rotary_scan.git
	cd ..
	catkin_make
	```
3. 下载安装[sick_scan](https://github.com/SICKAG/sick_scan)包
4. 配置环境变量  
`source devel/setup.bash`  
- 连接好硬件后运行  
`roslaunch rotary_scan rotary_scan.launch`  
- 或者运行模拟程序  
`roslaunch rotary_scan rotary_scan_sim.launch`  
该模拟程序模拟的是平移扫描，但原理和转动扫描是一致的

如果不能运行，进入rotary_scan的scripts文件夹，用`chmod +x filename.py`命令修改各python脚本的运行权限

### 硬件

1. 电机  
使用的是MOON's的TSM-23S-3RG步进伺服电机。电机接RS485-RS232转接口，再通过USB连接电脑。使用24V电源供电。  
#注意串口dev0  
[鸣志官网Windows软件](https://www.moons.com.cn/support-training/tools/Step_Servo)

2. 激光雷达
使用的是SICK公司的sick-lms-111激光雷达。通过网线连接电脑。使用24V电源供电。[如何设置网络？](https://www.cnblogs.com/21207-iHome/p/8022512.html)  
[SICK官网Windows软件SOPAS](https://www.sick.com/cn/zh/search?text=SOPAS)

## 二、rotary_scan的结构
![rqt_graph](rqt_graph.png)  
可以在运行程序时使用rqt_graph、rosnode、rostopic等工具了解程序的结构，具体用法查阅[ROS wiki](wiki.ros.org)  

以下从launch文件入手解释所运行的节点，各节点具体情况在子文件夹内说明

### rotary_scan.launch
- sick_scan 
引用了雷达的launch文件，该launch中运行的是`sick_lms_1xx`节点，负责读取雷达数据并发布PointCloud2格式的点云  
可以在sick_scan文件夹查看具体运行的代码，其中的launch文件中列举了可设置的雷达参数
- motor  
电机节点，负责控制电机转动，并通过查询电机的编码器来发布运动信息tf
- cloud_assembler_server  
点云合并服务节点，负责订阅雷达姐节点的点云和电机节点的tf，提供合并为点云的服务
- cloud_assembler_request  
点云合并请求节点，负责请求服务，并发布得到的合并结果
- rviz  
结果可视化节点

### rotary_scan_sim.launch
- bag_cloud  
播放节点，负责播放录制的雷达数据，发布点云
- motor
电机模拟节点，负责发布tf
- cloud_assembler_server  
提供点云合并服务
- cloud_assembler_request  
请求点云合并服务
- rviz  
结果可视化
