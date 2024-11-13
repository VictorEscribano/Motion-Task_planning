cmake_minimum_required(VERSION 3.8)
project(kautham_interfaces)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
# find_package(<dependency> REQUIRED)

set(msg_files
  "msg/PathVector.msg"
  "msg/Robconf.msg"
)

set(srv_files
  "srv/OpenProblem.srv"
  "srv/ProblemOpened.srv"
  "srv/CloseProblem.srv"
  "srv/SetRobControlsNoQuery.srv"
  "srv/ObsPos.srv"
  "srv/RobPos.srv"
  "srv/SetRobotsConfig.srv"
  "srv/RemoveRobot.srv"
  "srv/PathDofNames.srv"
  "srv/GetPath.srv"
  "srv/SetQuery.srv"
  "srv/DetachObstacle.srv"
  "srv/AttachObstacle2RobotLink.srv"
  "srv/CheckCollision.srv"
  "srv/SetPlannerParameter.srv"
  "srv/SetPlannerByName.srv"
)

set(kautham_interfaces_dependencies # Add packages that above message depend on
  "geometry_msgs"
  # "trajectory_msgs"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES ${kautham_interfaces_dependencies}
)

ament_export_dependencies(rosidl_default_runtime)

# Per poder utilitzar missatges i serveis creats en el mateix pkg (no necessari en aquest cas):
# rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
# target_link_libraries(<executable_name> "${cpp_typesupport_target}")

#rosidl_generate_interfaces(${PROJECT_NAME}_srv 
#"msg/Num.msg"
#"msg/Sphere.msg"
#"srv/AddThreeInts.srv" 
#DEPENDENCIES geometry_msgs # Add packages that above messages depend on, in this case geometry_msgs for Sphere.msg
#LIBRARY_NAME ${PROJECT_NAME}
#)

ament_package()
