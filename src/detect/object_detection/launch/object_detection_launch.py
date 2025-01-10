from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Declare launch arguments
    weights_arg = DeclareLaunchArgument('weights', default_value='sign.pt')
    conf_thres_arg = DeclareLaunchArgument('conf_thres', default_value='0.25')
    iou_thres_arg = DeclareLaunchArgument('iou_thres', default_value='0.45')
    device_arg = DeclareLaunchArgument('device', default_value='')
    img_size_arg = DeclareLaunchArgument('img_size', default_value='640')

    object_detect_node = Node(
        package='object_detection',
        executable='object_detection',
        # Pass launch arguments to node parameters
        parameters=[
            {'weights': LaunchConfiguration('weights')},
            {'conf_thres': LaunchConfiguration('conf_thres')},
            {'iou_thres': LaunchConfiguration('iou_thres')},
            {'device': LaunchConfiguration('device')},
            {'img_size': LaunchConfiguration('img_size')},
        ]
    
    )
    
    calibration_arg = DeclareLaunchArgument('calibration', default_value='False')

    camera_node = Node(
        package='camera',
        executable='H65_camera',
        parameters=[{'calibration': LaunchConfiguration('calibration')}]
    )

    # camera_node = Node(
    #     package='camera',
    #     executable='camera',
    # )
    
    # config=os.path.join(get_package_share_directory('detect_lane'), 'config', 'hsv_parameters_default.yaml')
    config=os.path.join(get_package_share_directory('detect_lane'), 'config', 'hsv_parameters_own.yaml')

    detect_node = Node(
        package='detect_lane',
        executable='detect_lane',
        parameters=[{'calibration': LaunchConfiguration('calibration')}, config],
    )

    hsv_node = Node(
        package='detect_lane',
        executable='hsv_param_adjustment',
        condition=IfCondition(LaunchConfiguration('calibration')),
    )

    

    # Create the launch description
    ld = LaunchDescription()

    # Add the launch arguments and nodes to the launch description
    ld.add_action(weights_arg)
    ld.add_action(conf_thres_arg)
    ld.add_action(iou_thres_arg)
    ld.add_action(device_arg)
    ld.add_action(img_size_arg)
    ld.add_action(object_detect_node)
    ld.add_action(core)
    ld.add_action(calibration_arg)
    ld.add_action(camera_node)
    ld.add_action(hsv_node)
    ld.add_action(detect_node)

    return ld



