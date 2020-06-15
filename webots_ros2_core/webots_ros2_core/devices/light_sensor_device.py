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

"""Webots LightSensor device wrapper for ROS2."""

from sensor_msgs.msg import Illuminance
from rclpy.time import Time
from rclpy.qos import qos_profile_sensor_data
from webots_ros2_core.math_utils import interpolate_lookup_table
from .device import Device


class LightSensorDevice(Device):
    """
    ROS2 wrapper for Webots LightSensor node.

    Creates suitable ROS2 interface based on Webots LightSensor node instance:
    https://cyberbotics.com/doc/reference/lightsensor

    It allows the following functinalities:
    - Publishes range measurements of type `sensor_msgs/Illuminance`

    Args:
        node (WebotsNode): The ROS2 node.
        wb_device (LightSensor): Webots node of type LightSensor.

    Kwargs:
        params (dict): Dictionary with configuration options in format of::

            dict: {
                'topic_name': str,      # ROS topic name (default will generated from the sensor name)
                'timestep': int,        # Publish period in ms (default is equal to robot's timestep)
                'disable': bool,        # Whether to create ROS interface for this sensor (default false)
                'always_publish': bool, # Publish even if there are no subscribers (default false)
            }

    """

    def __init__(self, node, wb_device, params=None):
        self._node = node
        self._wb_device = wb_device
        self._last_update = -1
        self._publisher = None

        # Determine default params
        params = params or {}
        self._topic_name = params.setdefault('topic_name', self._create_topic_name(wb_device))
        self._timestep = params.setdefault('timestep', int(node.robot.getBasicTimeStep()))
        self._disable = params.setdefault('disable', False)
        self._always_publish = params.setdefault('always_publish', False)

        # Create topics
        if not self._disable:
            self._publisher = self._node.create_publisher(
                Illuminance,
                self._topic_name,
                qos_profile_sensor_data
            )

    def step(self):
        if self._disable:
            return

        if self._node.robot.getTime() - self._last_update < self._timestep / 1e6:
            return
        self._last_update = self._node.robot.getTime()

        stamp = Time(seconds=self._node.robot.getTime()).to_msg()

        # Publish camera data
        if self._publisher.get_subscription_count() > 0 or self._always_publish:
            self._wb_device.enable(self._timestep)
            msg = Illuminance()
            msg.header.stamp = stamp
            msg.illuminance = interpolate_lookup_table(self._wb_device.getValue(
            ), self._wb_device.getLookupTable()) * IRRADIANCE_TO_ILLUMINANCE
            self._publisher.publish(msg)
        else:
            self._wb_device.disable()
