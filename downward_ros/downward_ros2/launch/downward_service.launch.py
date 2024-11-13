from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (
    LaunchConfiguration,
)
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):

    test_launch_arg = LaunchConfiguration('test')
    problem_launch_arg = LaunchConfiguration('problem')
    domain_launch_arg = LaunchConfiguration('domain')

    server_node = Node(
        package='downward_ros2',
        executable='service',
        name='service',
        arguments=[],
        parameters=[],
        output={'both': 'screen'},
    )

    client_node = Node(
        package='downward_ros2',
        executable='client',
        name='client',
        arguments=[],
        parameters=[
            {'problem_param': problem_launch_arg},
            {'domain_param': domain_launch_arg}
        ],
        output={'both': 'screen'},
        condition = IfCondition(test_launch_arg),
    )

    return [
        server_node,
        client_node,
    ]


def generate_launch_description():
    declared_arguments = []
    
    declared_arguments.append(
        DeclareLaunchArgument(
            'test',
            default_value='false',
            choices=('true', 'false'),
            description='launches the client to do a test if set to `true`.',
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'problem',
            default_value='block_world',
            #choices=('block_world', 'block_world_2', 'block_world_3', 'chess_world', 'chess_world_2', 'chess_world_3', 'etc...'),
            description='file name of a problem that uses the defined domain, e.g. problem:=block_world for the block_world domain or problem:=my_chess_world_problem for the chess_world domain',
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'domain',
            default_value='block_world',
            #choices=('block_world', 'chess_world'),
            description='domain file name, without the .pddl extension!!, e.g. domain:=block_world or domain:=chess_world',
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
