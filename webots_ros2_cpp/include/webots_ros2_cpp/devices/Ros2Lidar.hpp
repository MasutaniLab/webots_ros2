// Copyright 1996-2021 Cyberbotics Ltd.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef ROS2_LIDAR_HPP
#define ROS2_LIDAR_HPP

#include <map>
#include <webots/Lidar.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>
#include <sensor_msgs/msg/point_cloud.hpp>
#include <sensor_msgs/msg/channel_float32.hpp>
#include <webots_ros2_cpp/PluginInterface.hpp>
#include <webots_ros2_cpp/WebotsNode.hpp>


namespace webots_ros2
{
  class Ros2Lidar : public webots_ros2::PluginInterface
  {
  public:
    Ros2Lidar(webots_ros2::WebotsNode *node, std::map<std::string, std::string> &parameters);
    virtual void step(int size) override;

  private:
    void pubPointCloud();
    void pubLaserScan();

    webots::Lidar *mLidar;
    std::shared_ptr<webots_ros2::WebotsNode> mNode;
    std::map<std::string, std::string> mParameters;
    rclcpp::Publisher<sensor_msgs::msg::LaserScan>::SharedPtr mLaserPublisher;
    rclcpp::Publisher<sensor_msgs::msg::PointCloud>::SharedPtr mPointCloudPublisher;

    double mLastUpdate;

    std::string mTopicName;
    double mPublishTimestep;
    bool mAlwaysOn;
    int mPublishTimestepSyncedMs;
  };

} // end namespace webots_ros2

#endif
