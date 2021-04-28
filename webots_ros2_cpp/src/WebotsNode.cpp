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

#include <dlfcn.h>

#include "webots_ros2_cpp/WebotsNode.hpp"
#include "webots_ros2_cpp/PluginInterface.hpp"

namespace webots_ros2
{
  typedef std::shared_ptr<PluginInterface> (*creatorFunction)(webots_ros2::WebotsNode *node, const std::map<std::string, std::string> &parameters);

  WebotsNode::WebotsNode() : Node("webots_ros2_interface")
  {
  }

  void WebotsNode::init()
  {
    mRobot = std::make_unique<webots::Supervisor>();
    std::chrono::milliseconds ms((int)mRobot->getBasicTimeStep());
    mTimer = this->create_wall_timer(ms, std::bind(&WebotsNode::timerCallback, this));
  }

  std::string WebotsNode::fixedNameString(const std::string &name)
  {
    std::string fixedName = name;
    std::replace(fixedName.begin(), fixedName.end(), '-', '_');
    std::replace(fixedName.begin(), fixedName.end(), '.', '_');
    std::replace(fixedName.begin(), fixedName.end(), ' ', '_');
    std::replace(fixedName.begin(), fixedName.end(), ')', '_');
    std::replace(fixedName.begin(), fixedName.end(), '(', '_');
    return fixedName;
  }

  void WebotsNode::timerCallback()
  {
    mRobot->step(mStep);
    for (std::shared_ptr<PluginInterface> plugin : mPlugins)
      plugin->step(mStep);
  }

  void WebotsNode::registerPlugin(const std::string &pathToPlugin, const std::map<std::string, std::string> &arguments)
  {
    void *handle = dlopen(pathToPlugin.c_str(), RTLD_LAZY);
    if (!handle)
    {
      fprintf(stderr, "dlopen failure: %s\n", dlerror());
      exit(EXIT_FAILURE);
    }
    creatorFunction create = (creatorFunction)dlsym(handle, "create_plugin");

    std::shared_ptr<PluginInterface> plugin = (*create)(this, {{"name", "ds0"}});
    mPlugins.push_back(plugin);

    dlclose(handle);
  }

} // end namespace webots_ros2
