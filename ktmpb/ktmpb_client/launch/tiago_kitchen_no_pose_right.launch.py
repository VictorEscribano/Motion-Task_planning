from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.substitutions import (
    LaunchConfiguration,
)
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):

    tampconfigfile_arg = LaunchConfiguration('tampconfigfile')

    motion_server_node = Node(
        package='kautham_rosnode',
        executable='kautham_rosnode_server',
        name='kautham_rosnode_server',
        output={'both': 'screen'},
#        prefix=['xterm -e'],
     )
       
    task_server_node = Node(
        package='downward_ros2',
        executable='service',
        name='service',
        arguments=[],
        parameters=[],
        prefix=['xterm -e'],
    )

    ktmpb_client_node = Node(
        package='ktmpb_client',
        executable='ktmpb_python_interface',
        name='ktmpb_python_interface',
        arguments=[tampconfigfile_arg],
        parameters=[],
        output={'both': 'screen'},
    )

    return [
          motion_server_node,
          task_server_node,
          ktmpb_client_node,
    ]


def generate_launch_description():
    declared_arguments = []
    
    declared_arguments.append(
        DeclareLaunchArgument(
            'tampconfigfile',
            default_value="/demos/OMPL_geo_demos/Tiago-kitchen/tampconfig_no_pose_right.xml",
            description='launches the ktmpb client with the files set in the tampconfig file.',
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])