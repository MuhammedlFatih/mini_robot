from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
import launch_ros.actions  # Burada gerekli import
from ament_index_python.packages import get_package_share_directory
import os
from launch.conditions import IfCondition
from launch_ros.actions import Node  # Doğru import burada

def generate_launch_description():
    # URDF dosya yolu
    urdf_path = PathJoinSubstitution(
        [FindPackageShare('robot_vacuum'), 'urdf', 'main.xacro']
    )

    # Robot State Publisher node'u
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_path])}]
    )

    # Gazebo başlatma
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={'world': PathJoinSubstitution([FindPackageShare('robot_vacuum'), 'world', 'turtlebot3_world.world'])}.items()
    )

    # Robotu Gazebo'da spawn etme
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'robot_vacuum']
    )

    # RViz node'u
    rviz_config_path = PathJoinSubstitution(
        [FindPackageShare('robot_vacuum'), 'rviz', 'base_rviz.rviz']
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )


    # Launch description döndürme
    return LaunchDescription([
        robot_state_publisher,
        gazebo_launch,
        spawn_entity,
        rviz_node
    ])

