import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
import math
import os

# from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch
# from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

class LaserScanSubscriber(Node):

    def __init__(self):
        super().__init__('laser_scan_subscriber')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 100)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',  # 修改为你的激光雷达话题名称
            self.scan_callback,
            10)
        self.subscription  # 防止被Python清理掉

        msg_motor=Twist()
        msg_motor.linear.x=50.0
        msg_motor.angular.z=0.0
        self.publisher_.publish(msg_motor)
        time.sleep(2.5)


        
    def scan_callback(self, msg):
        distance_forward = self.find_distance_forward(msg)
        for i in distance_forward:
            self.get_logger().info('Distance at  degrees: %f' % i)
            if i<=0.3:
                self.get_logger().info('turn left' )
                msg_motor=Twist()
                msg_motor.linear.x=50.0
                msg_motor.angular.z=-9.0
                self.publisher_.publish(msg_motor)
                time.sleep(2.5)
                msg_motor.linear.x=50.0
                msg_motor.angular.z=0.0
                self.publisher_.publish(msg_motor)
                time.sleep(1)
                msg_motor.linear.x=-50.0
                msg_motor.angular.z=0.0
                self.publisher_.publish(msg_motor)
                time.sleep(1)
                msg_motor.linear.x=50.0
                msg_motor.angular.z=-9.0
                self.publisher_.publish(msg_motor)
                time.sleep(2.5)
                break
            else:
                self.get_logger().info('turn right' )
                msg_motor=Twist()
                msg_motor.linear.x=50.0
                msg_motor.angular.z=9.0
                self.publisher_.publish(msg_motor)
                time.sleep(2.5)
                msg_motor.linear.x=50.0
                msg_motor.angular.z=0.0
                self.publisher_.publish(msg_motor)
                time.sleep(1)
                msg_motor.linear.x=-50.0
                msg_motor.angular.z=0.0
                self.publisher_.publish(msg_motor)
                time.sleep(1)
                msg_motor.linear.x=50.0
                msg_motor.angular.z=9.0
                self.publisher_.publish(msg_motor)
                time.sleep(2.5)
                break

        




    def find_distance_forward(self, scan_msg):
        # 角度范围（弧度）
        angle_min = scan_msg.angle_min
        angle_max = scan_msg.angle_max

        # 角度增量（弧度）
        angle_increment = scan_msg.angle_increment

        # 距离列表
        ranges = scan_msg.ranges
        forward_degrees=[]
        idx_forward_degrees=[]
        distence=[]
        # 计算90度对应的索引

        for i in range(85,95):
            forward_degrees.append(math.radians(i))  # 将90度转换为弧度
            idx_forward_degrees.append(int((forward_degrees[i-85] - angle_min) / angle_increment))
            # 如果索引在范围内，则返回对应的距离；否则返回None
            if idx_forward_degrees[i-85] >= 0 and idx_forward_degrees[i-85] < len(ranges):
                # return ranges[idx_90_degrees]
                distence.append(ranges[idx_forward_degrees[i-85]])
            else:
                return None
        return distence
    

def main(args=None):
    rclpy.init(args=args)
    laser_scan_subscriber = LaserScanSubscriber()
    # laser_scan_subscriber.start_launch()
    rclpy.spin(laser_scan_subscriber)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
