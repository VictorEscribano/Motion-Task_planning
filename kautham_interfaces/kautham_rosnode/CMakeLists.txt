#https://github.com/bponsler/ros2-support/blob/master/tutorials/creating-a-mixed-cpp-and-python-package.md

cmake_minimum_required(VERSION 3.5)
project(kautham_rosnode)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install the python module for this package
ament_python_install_package(${PROJECT_NAME})

include_directories(include ${rclcpp_INCLUDE_DIRS})
link_directories(${rclcpp_LIBRARY_DIRS})

find_package(kautham_interfaces REQUIRED)
find_package(kautham CONFIG REQUIRED)
# - Config file for the Kautham package
# It defines the following variables
#  KAUTHAM_INCLUDE_DIRS - include directories for Kautham Lib
#  KAUTHAM_LIBRARIES    - libraries to link against Kautham Libs
#  KAUTHAM_LIBRARIES_STATIC - static version of the library
include_directories(${KAUTHAM_INCLUDE_DIRS})

#### MT ###############
set(mt_DIR include/libmt)
message (STATUS "Adding libmt directory ${mt_DIR}")
include_directories( ${mt_DIR} )
#### lcprng ###############
set(lcprng_DIR include/lcprng)
message (STATUS "Adding external directory ${lcprng_DIR} for lcprng.h")
include_directories( ${lcprng_DIR} )

add_executable(kautham_rosnode_server src/kautham_node.cpp)
target_link_libraries( kautham_rosnode_server ${KAUTHAM_LIBRARIES} )
#target_link_libraries( kautham_rosnode_server libkautham ${PUGI_XML_LIBRARIES} )
ament_target_dependencies(kautham_rosnode_server rclcpp kautham_interfaces kautham)


# Install C++ headers
install(
  DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.hpp")

install(TARGETS
    kautham_rosnode_server
    DESTINATION lib/${PROJECT_NAME})


# Install python scripts
install(PROGRAMS scripts/kautham_python_interface.py DESTINATION bin)
install(PROGRAMS scripts/kautham_client_python_node.py DESTINATION bin)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

# Export package dependencies
ament_export_dependencies(ament_cmake)
ament_export_dependencies(ament_cmake_python)
ament_export_dependencies(rclcpp)
ament_export_dependencies(rclpy)
ament_export_include_directories(include ${rclcpp_INCLUDE_DIRS})
ament_export_libraries(${PROJECT_NAME} ${rclcpp_LIBRARIES})


ament_package()
