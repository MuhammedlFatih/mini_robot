from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    configuration_directory = LaunchConfiguration('configuration_directory', default='/home/fatih/robot_ws/src/robot_vacuum/config')
    configuration_basename = LaunchConfiguration('configuration_basename', default='my_new_2d.lua')

    return LaunchDescription([
        DeclareLaunchArgument('configuration_directory', default_value=configuration_directory),
        DeclareLaunchArgument('configuration_basename', default_value=configuration_basename),

        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{
                'use_sim_time': False,
            }],
            arguments=['-configuration_directory', configuration_directory,
                       '-configuration_basename', configuration_basename],
        ),
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{
                'use_sim_time': False,
                'resolution': 0.05
            }],
        )
    ])
