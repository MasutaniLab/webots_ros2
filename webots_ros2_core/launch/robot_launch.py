#!/usr/bin/env python

# Copyright 1996-2020 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Launch Webots and ROS2 driver."""

import launch
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, EmitEvent, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from webots_ros2_core.utils import ControllerLauncher
from webots_ros2_core.webots_launcher import WebotsLauncher


ARGUMENTS = [
    DeclareLaunchArgument(
        'synchronization',
        default_value='False',
        description='If `False` robot.step() will be automatically called.'
    ),
    DeclareLaunchArgument(
        'package',
        default_value='webots_ros2_core',
        description='Package the package in which the node executable can be found.'
    ),
    DeclareLaunchArgument(
        'executable',
        default_value='webots_node',
        description='The name of the executable to find if a package is provided or otherwise a path to the executable to run.'
    ),
    DeclareLaunchArgument(
        'world',
        description='Path to Webots\' world file. Make sure `controller` field is set to `<extern>`.'
    ),
    DeclareLaunchArgument(
        'gui',
        default_value='True',
        description='Whether to start GUI or not.'
    ),
    DeclareLaunchArgument(
        'mode',
        default_value='realtime',
        description='Choose the startup mode (it must be either `pause`, `realtime`, `run` or `fast`).'
    ),
    DeclareLaunchArgument(
        'publish_tf',
        default_value='True',
        description='Whether to publish transforms (tf)'
    ),
    DeclareLaunchArgument(
        'node_parameters',
        description='Path to ROS parameters file that will be passed to the robot node'
    )
]


def generate_launch_description():
    synchronization = LaunchConfiguration('synchronization')
    package = LaunchConfiguration('package')
    executable = LaunchConfiguration('executable')
    world = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')
    mode = LaunchConfiguration('mode')
    publish_tf = LaunchConfiguration('publish_tf')
    node_parameters = LaunchConfiguration('node_parameters')

    # Webots
    webots = WebotsLauncher(
        world=world,
        mode=mode,
        gui=gui
    )

    # Driver node
    controller = ControllerLauncher(
        package=package,
        node_executable=executable,
        parameters=[
            node_parameters,
            {
                'synchronization': synchronization,
                'use_joint_state_publisher': publish_tf
            }],
        output='screen'
    )

    # Robot state publisher
    initial_robot_description = '<?xml version="1.0"?><robot name="dummy"><link name="base_link"></link></robot>'
    robot_state_publisher = Node(
        package='robot_state_publisher',
        node_executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': initial_robot_description}],
        condition=launch.conditions.IfCondition(publish_tf)
    )

    return LaunchDescription(ARGUMENTS + [
        robot_state_publisher,
        webots,
        controller,

        # Shutdown launch when Webots exits.
        RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])
