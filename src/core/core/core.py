import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int64, Bool
from enum import Enum

import launch
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription

def load_launch(launch_package, launch_name):
    launch_description = launch.LaunchDescription()
    launch_description.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([FindPackageShare(launch_package), '/launch', '/'+launch_name+'.py'])
        )
    )

    return launch_description

class Mode(Enum):
    LANE = 1
    INTERSECTION = 2
    OBSTACLES = 3
    PARKING = 4

class node(Node):
    def __init__(self):
        super().__init__('core_node')
        self.subscription_signs = self.create_subscription(String, '/detect/signs', self.signs_callback, 1)
        self.subscription_traffic_light = self.create_subscription(String, '/detect/traffic_light', self.traffic_light_callback, 1)
        self.subscription_yellow_fraction = self.create_subscription(Int64, '/detect/yellow_fraction', self.yellow_fraction_callback, 1) 
        self.subscription_white_fraction = self.create_subscription(Int64, '/detect/white_fraction', self.white_fraction_callback, 1) 
        self.subscription_parking_done = self.create_subscription(Bool, '/parking_done', self.parking_done_callback, 1)
        self.subscription_avoidance_done = self.create_subscription(Bool, '/avoidance_done', self.avoidance_done_callback, 1)

        self.subscription_signs
        self.subscription_traffic_light
        self.subscription_yellow_fraction
        self.subscription_white_fraction
        self.subscription_parking_done
        self.subscription_avoidance_done 

        #detect_lane:298
        self.publisher_which_line = self.create_publisher(Int64, '/detect/lane_mode', 1) #1:yellow" 2:white 0:all
        self.pub_stop = self.create_publisher(Bool, '/control/go_stop', 1) #true go 
        self.pub_lane_toggle = self.create_publisher(Bool, '/detect/lane_toggle', 1)
        
        self.mode = Mode.LANE
        self.traffic_light = String()

        self.lane_launch_ls = launch.LaunchService()
        lane_launch_description = load_launch('detect_lane', 'detect_lane_launch')
        self.lane_launch_ls.include_launch_description(lane_launch_description)
        
        self.parking_launch_ls = launch.LaunchService()
        parking_launch_description = load_launch('parking', 'parking_launch')
        self.parking_launch_ls.include_launch_description(parking_launch_description)

        self.avoidance_launch_ls = launch.LaunchService()
        avoidance_launch_description = load_launch('lider_sub', 'lider_sub_launch')
        self.avoidance_launch_ls.include_launch_description(avoidance_launch_description)


        

    def parking_done_callback(self, msg):
        self.parking_done = msg.data

        if self.parking_done == True:
            self.parking_launch_ls.shutdown()

    def avoidance_done_callback(self, msg):
        self.avoidance_done = msg.data

        if self.avoidance_done == True:
            self.avoidance_launch_ls.shutdown()
        
    def yellow_fraction_callback(self, msg):
        self.yellow_fraction = msg.data

    def white_fraction_callback(self, msg):
        self.white_fraction = msg.data

    def traffic_light_callback(self, msg):
        self.traffic_light = msg.data

    def signs_callback(self, msg):
        if msg.data == 'Ts':
            self.get_logger().info('Received: Intersection sign')
            #self.mode = Mode.INTERSECTION
            pass

        elif msg.data == 'left':
            self.get_logger().info('Received: LEFT sign')
            new_msg1=Int64()
            new_msg1.data=1
            self.publisher_which_line.publish(new_msg1)
        
        elif msg.data == 'right':
            self.get_logger().info('Received: RIGHT sign')
            new_msg2=Int64()
            new_msg2.data=2
            self.publisher_which_line.publish(new_msg2)

        elif msg.data == 'error':
            self.get_logger().info('Received: STOP sign')
            time. sleep (10)
            new_msg=Int64()
            new_msg.data=0
            self.publisher_which_line.publish(new_msg)
            # self.mode = Mode.LANE

        elif msg.data == 'dig':
            self.get_logger().info('Received: OBSTACLE sign')
            self.mode = Mode.OBSTACLES
            new_msg=Int64()
            new_msg.data=2
            self.publisher_which_line.publish(new_msg)
            time.sleep(35)
            stop_msg = Bool()
            stop_msg.data = False
            self.pub_stop.publish(stop_msg)
            # self.lane_launch_ls.shutdown()
            self.avoidance_launch_ls.run()
            stop_msg = Bool()
            stop_msg.data = True
            self.pub_stop.publish(stop_msg)# start 循線

        elif msg.data == 'park':
            self.get_logger().info('Received: PARKING sign')
            self.mode = Mode.PARKING
            new_msg=Int64()
            new_msg.data=0
            self.publisher_which_line.publish(new_msg)
            time.sleep(10)
            new_msg=Int64()
            new_msg.data=1
            self.publisher_which_line.publish(new_msg)
            time.sleep(10)
            self.parking_launch_ls.run()
            pass

        elif msg.data == 'row':
            self.get_logger().info('Received: STOPBAR sign')
            # pub stop car
            stop_msg = Bool()
            stop_msg.data = True
            self.pub_stop.publish(stop_msg)

        elif msg.data == 'cave':
            self.get_logger().info('Received: TUNNEL sign')
            self.mode = self.mode

        else:
            self.get_logger().info('Received: NONE sign')
            # self.lane_launch_ls.run() #test
            self.mode = self.mode


#==================================mode select===============================================
        if self.mode.value == Mode.LANE.value:
            self.get_logger().info('Mode: LANE')
            # self.lane_launch_ls.run()

        elif self.mode.value == Mode.INTERSECTION.value:
            self.get_logger().info('Mode: INTERSECTION')
            pass

        elif self.mode.value == Mode.OBSTACLES.value:
            self.get_logger().info('Mode: OBSTACLES')
            self.avoidance_launch_ls.run()

        elif self.mode.value == Mode.PARKING.value:
            self.get_logger().info('Mode: PARKING')
            self.parking_launch_ls.run()

def main(args=None):
    rclpy.init(args=args)
    core_node = node()
    rclpy.spin(core_node)
    core_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()