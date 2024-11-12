import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    package_dir = get_package_share_directory("arcanain_slam")
    #urdf = os.path.join(package_dir, "urdf" , "first_robot.urdf")
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    #world_path = os.path.join(package_dir, 'world', 'first_robot.sdf')
    map_path = os.path.join(package_dir, "map", 'map.yaml')
    nav_params_path = os.path.join(package_dir, "config", 'first_navigation.yaml')
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    #rviz = os.path.join(package_dir, "rviz" , "first_robot.rviz")
    rviz = os.path.join(package_dir, "rviz" , "nav2_default_view.rviz")
    #ekf_path = os.path.join(package_dir, "config", 'first_ekf.yaml')
    file_path = os.path.expanduser('~/ros2_ws/src/arcanain_simulator/urdf/mobile_robot.urdf.xml')

    with open(file_path, 'r') as file:
        robot_description = file.read()


    return LaunchDescription([
        
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', 'base_link', 'laser_frame']
            ),
        
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_path,
                'use_sim_time': use_sim_time,
                'params_file': nav_params_path}.items(),
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz],
            parameters=[{'use_sim_time': False}],
            output='screen'),
        
    ])