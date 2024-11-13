#!/usr/bin/env python3
import rclpy

#import rospkg
#import sys
#import kautham_interfaces
#from kautham_interfaces.srv import OpenProblem
#from kautham_interfaces.srv import CloseProblem
from kautham_interfaces.srv import *
from kautham_interfaces.srv import PathDofNames
from kautham_interfaces.srv import RobPos
from kautham_interfaces.srv import SetQuery 
from kautham_interfaces.srv import DetachObstacle 
from kautham_interfaces.srv import AttachObstacle2RobotLink 
from kautham_interfaces.srv import CheckCollision 
from kautham_interfaces.srv import SetPlannerParameter

#https://docs.ros.org/en/humble/How-To-Guides/Migrating-from-ROS1/Migrating-Python-Packages.html
## ROS1
## rospy.wait_for_service('add_two_ints')
## add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
## resp = add_two_ints(req)
# ROS2
#add_two_ints = node.create_client(AddTwoInts, 'add_two_ints')
#while not add_two_ints.wait_for_service(timeout_sec=1.0):
#    node.get_logger().info('service not available, waiting again...')
#resp = add_two_ints.call_async(req)
#rclpy.spin_until_future_complete(node, resp)

#Function that wraps the call to the kautham service that opens a problem
def kOpenProblem(node, modelFolder, problemFile):
    print(modelFolder)
    kthopenproblem_client = node.create_client(OpenProblem, '/kautham_node/OpenProblem')

    while not kthopenproblem_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('OpenProblem service not available, waiting again...')

    req = OpenProblem.Request()
    req.problem = problemFile
    #req.dir=[1]
    #req.dir[0] = modelFolder
    req.dir = [modelFolder]
    future= kthopenproblem_client.call_async(req)
    node.get_logger().info( "req.dir %s" % (req.dir[0]))
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    if result.response is True:
       node.get_logger().info( "Kautham Problem opened correctly" )
    else:
       node.get_logger().info( "ERROR Opening Kautham Problem" )
       node.get_logger().info( "models folder: %s" % (req.dir[0]) )
       node.get_logger().info( "problem file: %s" % (req.problem) )

    ## ROS1
    #print(modelFolder)
    #rospy.wait_for_service("/kautham_node/OpenProblem")
    #kthopenproblem_srv = OpenProblem()
    #kthopenproblem_srv.problem = problemFile
    #kthopenproblem_srv.dir=[1]
    #kthopenproblem_srv.dir[0] = modelFolder

    #kthopenproblem_client =rospy.ServiceProxy("/kautham_node/OpenProblem", OpenProblem)
    #k=kthopenproblem_client(kthopenproblem_srv.problem, kthopenproblem_srv.dir)
    #if k.response is True:
    #    rospy.loginfo( "Kautham Problem opened correctly" )
    #else:
    #    rospy.logerr( "ERROR Opening Kautham Problem" )
    #    rospy.logerr( "models folpder: %s", kthopenproblem_srv.dir[0] )
    #    rospy.logerr( "problem file: %s", kthopenproblem_srv.problem)


# Function that wraps the call to the kautham service that closes a problem
def kCloseProblem(node):
    kthcloseproblem_client = node.create_client(CloseProblem, '/kautham_node/CloseProblem')

    req = CloseProblem.Request()
    while not kthcloseproblem_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('CloseProblem service not available, waiting again...')
    future=kthcloseproblem_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    #result = future.result()
    print( "Kautham Problem closed")

    ## ROS1
    #rospy.wait_for_service("/kautham_node/CloseProblem")
    #kthcloseproblrm_srv = CloseProblem()
    #kthcloseproblrm_client = rospy.ServiceProxy("/kautham_node/CloseProblem", CloseProblem)
    #kthcloseproblrm_client()
    #print( "Kautham Problem closed")

#Function that wraps the call to the kautham service that sets the control file for the robot
def kSetRobControlsNoQuery(node, controls):
    kthsetrobcontrolnoquery_client = node.create_client(SetRobControlsNoQuery, '/kautham_node/SetRobControlsNoQuery')

    req = SetRobControlsNoQuery.Request()
    req.controls = controls
    while not kthsetrobcontrolnoquery_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('SetRobControlsNoQuery service not available, waiting again...')
    future = kthsetrobcontrolnoquery_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()
    if r.response:
        print("Controls set ok")
    else:
        print("Set Controls failed")
    return (r.response)

#Function that wraps the call to the kautham service that sets the position of obstcle
def kSetObstaclePos(node, obsname, setpos):
    kthsetobstaclepos_client = node.create_client(ObsPos, '/kautham_node/SetObstaclePos')

    req = ObsPos.Request()
    print(obsname)
    req.obsname = obsname
    print(setpos)
    req.setpos = setpos
    while not kthsetobstaclepos_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('ObsPos service not available, waiting again...')
    future=kthsetobstaclepos_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()
    if r.response:
        print("Obstacle Set")
    else:
        print("Set obstacle failed")
    return (r.response)


# Function that wraps the call to the kautham service that moves the robot
def kMoveRobot(node, controls):
    kthsetrobotsconfig_client = node.create_client(SetRobotsConfig, '/kautham_node/SetRobotsConfig')

    req = SetRobotsConfig.Request()
    req.controls = controls
    while not kthsetrobotsconfig_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('SetRobotsConfig service not available, waiting again...')
    future = kthsetrobotsconfig_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()
    if r.response:
        print("Robot(s) Moved correctly")
    else:
        print("ERROR failed moveRobot")
    return r.config

#Function that wraps the call to the kautham service returns Dof names
def kPathDofNames(node):
    pathdofnames_client = node.create_client(PathDofNames, '/kautham_node/PathDofNames')

    req = PathDofNames.Request()
    while not pathdofnames_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('PathDofNames service not available, waiting again...')
    future = pathdofnames_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()
    
    return r.dofnames

#Function that wraps the call to the kautham service that gets the pose of a robot
def kGetRobotPos(node, indexrob):
    kthrobotpos_client = node.create_client(RobPos, '/kautham_node/GetRobotPos')

    req = RobPos.Request()
    req.index= indexrob
    req.setpos = ( 20.0, 70.0, 40.0, 0.0, 0.0, 0.0, 1.0 )#Dummy for python error fix?
    while not kthrobotpos_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('GetRobotPos service not available, waiting again...')
    future = kthrobotpos_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()
    if len(r.getpos)>0:
        print("Robot position = ", r.getpos)
    else:
        print("No position returned")
        #return False #!!?
    return r.getpos


#Function that wraps the call to the kautham service that solves a problem
def kGetPath(node, printpath=0):
    kthgetpath_client = node.create_client(GetPath, '/kautham_node/GetPath')
    
    req = GetPath.Request()
    while not kthgetpath_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('GetPath service not available, waiting again...')
    future = kthgetpath_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()
    if len(r.response) == 0:
        print ("No path found")
        return False
    else:
        print ("Path Found")
        length = len(r.response)
        path = { (i,j):0 for i in range(length) for j in range(len(r.response[0].v)) }
        for i in range(length):
            #if printpath: print(i,"- len",len(getpath_srv.response[i].v))
            for j in range(len(r.response[i].v)):
                path[i,j]=r.response[i].v[j]
                if printpath: print(round(path[i,j],3), end=" ")
            if printpath: print()
        return path


# Function that wraps the call to the kautham service that sets a new query to be solved
def kSetQuery(node, init,goal):
    kthsetquery_client = node.create_client(SetQuery, '/kautham_node/SetQuery')

    req = SetQuery.Request()
    req.init = init
    req.goal = goal
    while not kthsetquery_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('SetQuery service not available, waiting again...')
    future = kthsetquery_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    if r.response is False:
        print("Query has not been set")
    return r.response

# Function that wraps the call to the kautham service that attaches an object to a given link
def kAttachObject(node, robotnumber, linknumber, obsname):
    kthattachonject_client = node.create_client(AttachObstacle2RobotLink, '/kautham_node/AttachObstacle2RobotLink')
    
    req = AttachObstacle2RobotLink.Request()
    req.robot = robotnumber
    req.link = linknumber
    req.obs = obsname
    while not kthattachonject_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('AttachObstacle2RobotLink service not available, waiting again...')
    future = kthattachonject_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    print("Attached object",end=" ")
    print(obsname,end=" ")
    print("to link",end=" ")
    print(linknumber,end=" ")
    print("of robot",end=" ")
    print(robotnumber)
    return r.response

# Function that wraps the call to the kautham service that dettaches an attached object
def kDetachObject(node, obsname):
    kthdetachobject_client = node.create_client(DetachObstacle, '/kautham_node/DetachObstacle')

    req = DetachObstacle.Request()
    req.obsname = obsname
    while not kthdetachobject_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('DetachObstacle service not available, waiting again...')
    future = kthdetachobject_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    print ("Detached object",end=" ")
    print(obsname)
    return r.response

#Function that wraps the call to the kautham service that gets the pose of an obstacle
def kGetObstaclePos(node, obsname):
    kthgetobstacle_client = node.create_client(ObsPos, '/kautham_node/GetObstaclePos')

    req = ObsPos.Request()
    req.obsname = obsname
    while not kthgetobstacle_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('GetObstaclePos service not available, waiting again...')
    future = kthgetobstacle_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    if len(r.getpos)>0:
        print("obstacle position = ", r.getpos)
    else:
        print("No position returned")
        return False
    return (r.getpos)

# Function that wraps the call to the kautham service that checks for collision
def kIsCollisionFree (node, controls):
    kthcheckcollision_client = node.create_client(CheckCollision, '/kautham_node/CheckCollision')

    req = CheckCollision.Request()
    req.config = controls
    while not kthcheckcollision_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('CheckCollision service not available, waiting again...')
    future = kthcheckcollision_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    print("kIsCollisionFree msg: ", r.msg)
    return r.collisionfree

# Function that wraps the call to the kautham service that sets the planner parameters
def kSetPlannerParameter(node, parametername, paramatervalue):
    kthsetplannerparameter_client = node.create_client(SetPlannerParameter, '/kautham_node/SetPlannerParameter')

    req = SetPlannerParameter.Request()
    req.parameter = parametername
    req.value = paramatervalue
    while not kthsetplannerparameter_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('SetPlannerParameter service not available, waiting again...')
    future = kthsetplannerparameter_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    return r.response







