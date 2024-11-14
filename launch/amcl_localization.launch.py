import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    package_dir = get_package_share_directory("arcanain_slam")
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_file = os.path.join(package_dir, "map", 'map.yaml')
    print(map_file)
    amcl_params_path = os.path.join(package_dir, "config", 'amcl_params.yaml')
    rviz = os.path.join(package_dir, "rviz" , "nav2_default_view.rviz")

    file_path = os.path.expanduser('~/ros2_ws/src/arcanain_simulator/urdf/mobile_robot.urdf.xml')
    with open(file_path, 'r') as file:
        robot_description = file.read()


    return LaunchDescription([
        
        # 地図サーバーノードの起動
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'yaml_filename': map_file, 'use_sim_time': True}]
        ),
        
        # AMCLノードの起動
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[amcl_params_path, {'use_sim_time': False}]
        ),
        
        # 静的なTF変換 (base_link -> laser_frame)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['0.0', '0.0', '0.2', '0.0', '0.0', '0.0', 'base_link', 'laser_frame']  # 位置は仮の値で調整が必要です
        ),
        # RViz2の起動
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz],
            parameters=[{'use_sim_time': False}],
            output='screen'
        ),
        
    ])
