from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
   return LaunchDescription([
       Node(
           package='kautham_rosnode',
           #namespace='kth',
           executable='kautham_rosnode_server',
           name='kautham_rosnode_server',
           output="screen"
       )
   ])
