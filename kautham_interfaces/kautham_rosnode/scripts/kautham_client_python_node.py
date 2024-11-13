#!/usr/bin/env python3
import rclpy
import kautham_python_interface as kautham
import xml.etree.ElementTree as ET

import sys


#def main(args=None):
#    rclpy.init(args=args)

def main():
    rclpy.init(args=None)
    node = rclpy.create_node('kautham_python_client')

    #Open config file
    #root_demo_folder = "/home/polrc/ioc/kautham"
    #root_demo_folder = "/usr/local/share/kautham"
    #root_demo_folder = "/home/janrosell/ros2/ros2_wsKauthamFixedBug/src/kautham"
    root_demo_folder = "/usr/share/kautham"
    configfile = root_demo_folder+"/demos/OMPL_geo_demos/chess/kthconfig.xml"
    modelFolder = root_demo_folder+"/demos/models/"
    #check for arguments
    args = sys.argv[1:] # args is a list of the command line args
    if len(args)==1 or len(args)>2:
        print("Erroneous number of args")
        print("Use two arguments to define the root_demo_folder and the ktconfig file, e.g. ")
        print("    $./kautham_client_python_node.py /usr/local/share/kautham /demos/OMPL_geo_demos/chess/kthconfig.xml")
        print("No arguments required to used the default values: /usr/share/kautham and /demos/OMPL_geo_demos/chess/kthconfig.xml")
        return
    if len(args)==2:
        root_demo_folder = args[0]
        configfile = root_demo_folder+args[1]
        modelFolder = root_demo_folder+"/models/"
    print("\n++++++++++++++++++++++++++++++++++++++")
    print("Using root_demo_folder:", root_demo_folder)
    print("Using kthconfig file:", configfile)
    print("You can change them by passing arguments, e.g. ")
    print("    $./kautham_client_python_node.py /usr/local/share/kautham /demos/OMPL_geo_demos/chess/kthconfig.xml")
    
    #Problem file:
    config_tree = ET.parse(configfile)
    config_root = config_tree.getroot()
    kauthamproblem = config_root.find('Problemfiles').find('kautham').get('name')
    kthconfig_directory =config_root.find('Problemfiles').find('directory').get('name')
    print("\n++++++++++++++++++++++++++++++++++++++")
    print("Using kautham problem defined in the kthconfig file: ",kauthamproblem)
    #Setting problem files
    root_problem_folder = root_demo_folder + kthconfig_directory
    kauthamProblemFile = root_problem_folder + kauthamproblem
    node.get_logger().info(
        'Kautham Problem File: %s' %
        (kauthamProblemFile))
    
    #Open kautham problem
    print("\n***************************************")
    print("   Opening problem                     ")
    print("***************************************")
    kautham.kOpenProblem(node,modelFolder, kauthamProblemFile)

    print("\n***************************************")
    print("   Get Path                            ")
    print("***************************************")
    #<Init>0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5</Init>
	#<Goal>0.662338 0.271613 0.760218 0.722817 0.738732 0.659155 0.676090 0.643239 0.213521 0.770563 0.245352 0.261268 0.500000 0.600000</Goal>
    path=kautham.kGetPath(node,1) #do print path when calling kGetPath
    #print("PATH = ", path)

    print("\n***************************************")
    print("   Set query                           ")
    print("***************************************")
    init = (1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    goal = (0.662338, 0.271613, 0.760218, 0.722817, 0.738732, 0.659155, 0.676090, 0.643239, 0.213521, 0.770563, 0.245352, 0.261268, 0.500000, 0.600000)
    print("Init = ", init)
    print("Goal = ", goal)
    path=kautham.kSetQuery(node,init,goal) 

    print("\n***************************************")
    print("   Set Planner and planner parameters  ")
    print("***************************************")
    print("Setting omplRRTConnect planner with Range 0.7")
    kautham.kSetPlannerByName(node, "omplRRTConnect") #to new range from 0.5 to 0.7
    kautham.kSetPlannerParameter(node, "Range", "0.7") #to new range from 0.5 to 0.7

    print("\n***************************************")
    print("   Get Path Again                      ")
    print("***************************************")
    path=kautham.kGetPath(node,1) #do print path when calling kGetPath

    print("\n***************************************")
    print("   Check DOF names                     ")
    print("***************************************")
    dofnames = kautham.kPathDofNames(node)
    print(dofnames)

    print("\n***********************************************************************")
    print("   Setting the two robot to a configuration specified by the controls  ")
    print("***********************************************************************")
    controls = (0.662338, 0.271613, 0.760218, 0.722817, 0.738732, 0.659155, 0.676090, 0.643239, 0.213521, 0.770563, 0.245352, 0.261268, 0.500000, 0.600000)
    print("Robot controls: ", controls)
    kautham.kMoveRobot(node, controls)

    print("\n********************************************************************")
    print("   Check collision at config to pick object                         ")
    print("********************************************************************")
    controls = (0.587, 0.337, 0.698, 0.698, 0.746, 0.587, 0.44, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5) #configuration to grasp the object
    kautham.kIsCollisionFree (node, controls)

    print("\n********************************************************")
    print("   Setting the control file to just move robot 0        ")
    print("********************************************************")
    robot_control_file = "controls/ur3_robotniq_A.cntr"
    print("control file: " + robot_control_file)
    kautham.kSetRobControlsNoQuery(node, robot_control_file)

    print("\n********************************************************************")
    print("   Check collision at config to pick object                         ")
    print("********************************************************************")
    controls = (0.587, 0.337, 0.698, 0.698, 0.746, 0.587, 0.44) #configuration to grasp the object
    kautham.kIsCollisionFree (node, controls)

    print("\n********************************************************************")
    print("   Moving the robot 0 to a configuration to pick object             ")
    print("********************************************************************")
    controls = (0.587, 0.337, 0.698, 0.698, 0.746, 0.587, 0.44) #configuration to grasp the object
    print("Set Robot 0 to configuration specified by controls: ", controls)
    kautham.kMoveRobot(node, controls)

    print("\n***************************************")
    print("   Getting the pose of pawnB1          ")
    print("***************************************")
    obspos=kautham.kGetObstaclePos(node, "pawnB1")
    print("pawnB1 pose=", obspos)

    print("\n***************************************************")
    print("   Attaching pawnB1 to robot 0 gripper base        ")
    print("***************************************************")
    robotIndex = 0
    linkIndex = 10 #gripper_base ?
    kautham.kAttachObject(node, robotIndex, linkIndex, "pawnB1")

    print("\n********************************************************************")
    print("   Moving the robot 0 to place configuration                        ")
    print("********************************************************************")
    controls = (0.782, 0.337, 0.698, 0.698, 0.746, 0.52, 0.44) #configuration to place object
    print("Set Robot 0 to configuration specified by controls: ", controls)
    kautham.kMoveRobot(node, controls)

    print("\n***************************************************")
    print("   Dettach pawnB1                                  ")
    print("***************************************************")
    kautham.kDetachObject(node, "pawnB1")

    print("\n***************************************")
    print("   Getting the pose of pawnB1          ")
    print("***************************************")
    obspos=kautham.kGetObstaclePos(node, "pawnB1")
    print("pawnB1 pose=", obspos)

    print("\n***************************************")
    print("   Getting the pose of robot 0         ")
    print("***************************************")
    robotIndex=0
    robotpos=kautham.kGetRobotPos(node, robotIndex)
    print("robot0 pose=", robotpos)

    print("\n***************************************")
    print("   Getting the pose of robot 1         ")
    print("***************************************")
    robotIndex=1
    robotpos=kautham.kGetRobotPos(node, robotIndex)
    print("robot1 pose=", robotpos)

    print("\n***************************************")
    print("   Moving object pawnB1                ")
    print("***************************************")
    poseobject = (0.025, 0.025, 0.02, 0.0, 0.0, 1.0, 0.0)#in axis-angle
    print("PawnB1 pose = ", poseobject)
    kautham.kSetObstaclePos(node,"pawnB1",poseobject)

    print("\n***************************************")
    print("   Getting the pose of pawnB1          ")
    print("***************************************")
    obspos=kautham.kGetObstaclePos(node, "pawnB1")
    print("pawnB1 pose=", obspos)

    print("\n***************************************")
    print("   Closing problem                     ")
    print("***************************************")
    kautham.kCloseProblem(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
