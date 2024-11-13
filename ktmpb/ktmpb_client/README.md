# ROS client for Flexibly configuring task and motion planning problems

A planning framework for both levels of planning that includes an easy way to configure their interconnection. Motion planning is done using The Kautham Project, which is equipped with the Open Motion Planning Library suite of sampling-based motion planners,and task planning is done using the Fast Forward task planner. Both planning levels are acessible through Robotic Operating System interfaces using services. A client program then uses these task and motion planning services and an XML configuration file that defines the linkage between symbolic actions and geometric values, to compute the sequence of feasible robot motions that allow to successfully execute a manipulation task.

## Requirements

- ROS2 Humble 
- The motion planner (The Kautham Project)
- The task planner (Fast-downward)  
- The motion planning server (kautham_interfaces)
- The task planning server (downward_ros2)  
- The task and motion planning client (this project)
- (optional) Tiago arm kinematics

## Installation instructions

### ROS2 Humble 

### The Kautham Project

### The Fast Downward Task Planner

## Build instructions

### The Kautham Interfaces package

### The Downward_ros package

### The task and motion planning client

# Running the example
#### Tiago-kitchen example with robot configuration

Run the Tiago-Kitchen example that uses the `tampconfig_no_pose_right.xml` file that sets the grasping configurations for pick and place as vectors of (joint) controls:

```
$ roslaunch ktmpb tiago_kitchen_no_pose_right.launch
```

#### Verify with Kautham GUI
Run the Kautham GUI and verify the solution:
```
$ kautham_gui
```

- Open the `tiago_mobile_counterA_counterB.xml` problem in the Kautham GUI
- Load the taskfile `taskfile_tampconfig_pose_no_graspit_right.xml`
- Click on start move


![Alt text](gif/tiago-kitchen-video.gif)


#### Making changes to the task and motion planning problem

The`tampconfig.xml` file can be modified for creating different instances of the manipulation tasks. 

For instance, if Tiago arm kinamatics package is installed, we can use the `tampconfig_pose_right.xml` file that sets the grasping configurations for pick and place as poses:

- The Graspcontrols tags in the PICK and PLACE actions are commented.
- The Pose tag is uncommented to set the pose to PICK the object.
- The Poseregion tag is uncommented to set the pose to PLACE the object.

Run the Tiago-Kitchen example with poses:
```
$ roslaunch ktmpb tiago_kitchen_pose_right.launch
```

