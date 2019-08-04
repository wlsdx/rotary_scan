# motor  
串口通信，并且读取编码器位置，根据位置计算并发布tf  
终止扫描目前采用判据的是IE>20000，即转过一圈  
详细内容在源码中有注释

电机控制指令是SCL，详见[文档](../../files/Host-Command-Reference_920-0002P.PDF)  
串口通信格式：波特率9600，数据位8，校验位无，注意串口，换行符\r\n(CRLF)，默认串口是/dev/ttyUSB0  
电机一转是20000脉冲。`1IE`指令可以得到以脉冲数记录的位置信息，通过计算该位置可以得到电机转动的位置

tf树：fixed_frame是'base_link'，雷达的link名是'laser'  
tf信息和实际位姿的关系请查万能的ROS wiki和文档

# assemble_requset
向laser_assembler请求服务并发布结果的点云  
详细内容在源码中有注释
