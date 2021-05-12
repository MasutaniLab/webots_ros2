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

#ifndef ROS2_RANGE_FINDER_HPP
#define ROS2_RANGE_FINDER_HPP

#include <map>
#include <sensor_msgs/msg/camera_info.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <webots/RangeFinder.hpp>
#include <webots_ros2_cpp/devices/Ros2SensorPlugin.hpp>
#include <webots_ros2_cpp/WebotsNode.hpp>


namespace webots_ros2
{

  class Ros2RangeFinder : public Ros2SensorPlugin
  {
  public:
    void init(webots_ros2::WebotsNode *node, std::map<std::string, std::string> &parameters) override;
    void step() override;

  private:
    void publishImage();

    webots::RangeFinder* mRangeFinder;
    webots_ros2::WebotsNode *mNode;

    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr mImagePublisher;
    sensor_msgs::msg::Image mImageMessage;
    rclcpp::Publisher<sensor_msgs::msg::CameraInfo>::SharedPtr mCameraInfoPublisher;
    sensor_msgs::msg::CameraInfo mCameraInfoMessage;

    std::string mTopicName;
    std::string mFrameName;
    double mPublishTimestep;
    bool mAlwaysOn;
    int mPublishTimestepSyncedMs;

    double mLastUpdate;
    bool mIsEnabled;
  };

}

#endif
