import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir

def generate_launch_description():
    # Konfigürasyonlar
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    # Kendi robotunuzun Cartographer konfigürasyonlarının bulunduğu dizin
    my_robot_cartographer_prefix = get_package_share_directory('robot_vacuum')
    cartographer_config_dir = LaunchConfiguration('cartographer_config_dir', default=os.path.join(
                                                  my_robot_cartographer_prefix, 'config'))
    
    # Cartographer için konfigürasyon dosyasının adı
    configuration_basename = LaunchConfiguration('configuration_basename', default='my_2d.lua')
    
    # # RViz dosyasının konumu
    # rviz_config_dir = os.path.join(get_package_share_directory('robot_vacuum'),
    #                                'rviz', 'my_robot_cartographer.rviz')
    
    # Harita çözünürlüğü
    resolution = LaunchConfiguration('resolution', default='0.05')

    # Harita yayınlama periyodu
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')

    return LaunchDescription([
        # Cartographer konfigürasyon dosyasının yolunu belirt
        DeclareLaunchArgument(
            'cartographer_config_dir',
            default_value=cartographer_config_dir,
            description='Full path to config file to load'),
        
        # Lua konfigürasyon dosyasının adını belirt
        DeclareLaunchArgument(
            'configuration_basename',
            default_value=configuration_basename,
            description='Name of lua file for cartographer'),
        
        # Simülasyon zamanını kullanıp kullanmayacağınızı belirtin
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        # Cartographer node'u başlat
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename]),

        # OccupancyGrid için çözünürlük parametresi
        DeclareLaunchArgument(
            'resolution',
            default_value=resolution,
            description='Resolution of a grid cell in the published occupancy grid'),

        # Harita yayınlama periyodu
        DeclareLaunchArgument(
            'publish_period_sec',
            default_value=publish_period_sec,
            description='OccupancyGrid publishing period'),

        # OccupancyGrid Launch Dosyasını Dahil Et
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/occupancy_grid.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time, 'resolution': resolution,
                              'publish_period_sec': publish_period_sec}.items(),
        ),
        
        # # RViz konfigürasyon dosyasını başlat (eğer gerekiyorsa)
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen',
        #     arguments=['-d', rviz_config_dir],
        #     parameters=[{'use_sim_time': use_sim_time}],
        # ),
    ])
