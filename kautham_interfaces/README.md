# kautham_interfaces


[kautham_interfaces](https://gitioc.upc.edu/rostutorials/kautham_interfaces.git) is a C++ ROS server of [Kautham](https://github.com/iocroblab/kautham.git).

A client node is also available to test the services.


## Service Calls

The file **kautham_python_interface.py** offers the functions that do the service calls.

  - kOpenProblem 
  - kCloseProblem 
  - kSetRobControlsNoQuery 
  - kSetObstaclePos 
  - kGetObstaclePos
  - kMoveRobot
  - kGetRobotPos
  - kPathDofNames 
  - kGetPath
  - kSetQuery
  - kDetachObject 
  - kAttachObject 
  - kIsCollisionFree 
  - kSetPlannerParameter

## Test

The file **kautham_client_python_node.py** is the client node that, using a default demo problem, checks the calls to all the services.

1. Opens the Chess problem with two UR3 robots:  
        kautham.kOpenProblem(node,modelFolder, kauthamProblemFile)
2. Solves the path for the default query:  
        path=kautham.kGetPath(node,1) 
3. Changes the query: 
        path=kautham.kSetQuery(node,init,goal) 
4. Changes some planner parameters:
        kautham.kSetPlannerParameter(node, "Range", "0.7")
        kautham.kSetPlannerParameter(node, "_Incremental (0/1)", "0") 
5. Solves the path for the new query: 
        path=kautham.kGetPath(node,1) 
6. Checks the names of the robot joints:
        dofnames = kautham.kPathDofNames(node)
7. Sets the configuration of the robots A and B: 
        kautham.kMoveRobot(node, controls)
8. Checks for collision for the given robots configuration:
        kautham.kIsCollisionFree (node, controls)
9. Changes the control file (to control just robot A)
        kautham.kSetRobControlsNoQuery(node, robot_control_file)
10. Checks for collision for the given configuration of robot A:
        kautham.kIsCollisionFree (node, controls)
11. Sets the configuration of robot A: 
        kautham.kMoveRobot(node, controls)
12. Get the pose of the pawnB1 object:
        obspos=kautham.kGetObstaclePos(node, "pawnB1")
13. Attach the pawn to the gripper of robot A: 
        kautham.kAttachObject(node, robotIndex, linkIndex, "pawnB1")
14. Sets the configuration of robot A: 
        kautham.kMoveRobot(node, controls)
15. Detach the object:
        kautham.kDetachObject(node, "pawnB1")
16. Get the (new) pose of the pawnB1 object:
        obspos=kautham.kGetObstaclePos(node, "pawnB1")
17. Get the base pose of the robot A:
        robotpos=kautham.kGetRobotPos(node, robotIndex)
18. Get the base pose of the robot AB:
        robotpos=kautham.kGetRobotPos(node, robotIndex)
19. Change the pose of the pawnB1:
        kautham.kSetObstaclePos(node,"pawnB1",poseobject)
20. Check the (new) pose of the pawnB1 object:
        obspos=kautham.kGetObstaclePos(node, "pawnB1")
21. Close problem:
        kautham.kCloseProblem(node)

## Build Package

```
$ colcon build
$ source install/local_setup.bash
```

## Run Test

Run the server:

```
$ ros2 launch kautham_rosnode kautham_rosnode.launch.py
```

Run the client with the chess problem (default): 

```
$ kautham_client_python_node.py
```

Run the client with another problem: Use two arguments to define the **root_demo_folder** and the **ktconfig file**, e.g.:


```
$ kkautham_client_python_node.py /usr/local/share/kautham /demos/OMPL_geo_demos/chess/kthconfig.xml
```