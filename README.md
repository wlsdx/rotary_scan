# rotary_scan
用步进电机带动激光雷达转动，在ROS上控制并得到转动扫描的结果  

![structure](/files/structure.png)

## 一、如何使用rotary_scan
### 软件

1. 安装[ROS kinetic](https://wiki.ros.org/kinetic/Installation) （操作系统建议使用和开发时一致的Ubuntu 16.04）
2. 将rotary_scan文件夹复制到catkin工作空间的src文件夹，编译，修改脚本运行权限，例：  
	```
	mkdir -p catkin_ws/src
	git clone https://github.com/wlsdx/rotary_scan/rotary_scan.git
	mv rotary_scan/rotary_scan catkin_ws/src/rotary_scan
	cd catkin_ws
	catkin_make
	chmod +x src/rotary_scan/scripts -R
	```
3. 下载安装[sick_scan](https://github.com/SICKAG/sick_scan)包
4. 配置环境变量  
`source catkin_ws/devel/setup.bash`  
- 连接好硬件后运行  
`roslaunch rotary_scan rotary_scan.launch`  
- 或者运行模拟程序  
`roslaunch rotary_scan rotary_scan_sim.launch`  
该模拟程序模拟的是平移扫描，但原理和转动扫描是一致的

模拟扫描结果：红线是雷达轨迹，右侧是电脑台![result](/files/keyboard.png)

如果不能运行：
- 检查雷达的IP（可以用ping或者用Windows程序SOPAS），在rotary_scan.launch中修改hostname
- 检查串口名，在motor.py中修改

### 硬件
![mechanical](/files/mechanical.JPG)

1. 电机  
使用的是MOON's的TSM-23S-3RG步进伺服电机。电机接RS485-RS232转接口，再通过USB连接电脑。使用24V电源供电。  
[鸣志官网Windows软件](https://www.moons.com.cn/support-training/tools/Step_Servo)

2. 激光雷达
使用的是SICK公司的sick-lms-111激光雷达。通过网线连接电脑。使用24V电源供电。[如何设置网络？](https://www.cnblogs.com/21207-iHome/p/8022512.html)  
[SICK官网Windows软件SOPAS](https://www.sick.com/cn/zh/search?text=SOPAS)

## 二、rotary_scan的结构
![node_graph](/files/node_graph.png)  
可以在运行程序时使用rqt_graph、rosnode、rostopic等工具了解程序的结构，具体用法查阅[ROS wiki](wiki.ros.org)  

以下从launch文件入手解释所运行的节点

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

## 三、主要节点
### motor  
串口通信，并且读取编码器位置，根据位置计算并发布tf  
终止扫描目前采用判据的是IE>20000，即转过一圈  
详细内容在源码中有注释

电机控制指令是SCL，详见[文档](/files/Host-Command-Reference_920-0002P.PDF)  
串口通信格式：波特率9600，数据位8，校验位无，注意串口，换行符\r\n(CRLF)，默认串口是/dev/ttyUSB0  
电机一转是20000脉冲。`1IE`指令可以得到以脉冲数记录的位置信息，通过计算该位置可以得到电机转动的位置

tf树：fixed_frame是'base_link'，雷达的link名是'laser'  
tf信息和实际位姿的关系请查万能的ROS wiki和文档

### assemble_requset
向laser_assembler请求服务并发布结果的点云  
详细内容在源码中有注释
