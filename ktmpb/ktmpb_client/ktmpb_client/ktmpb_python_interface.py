#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

#to get the package path:
from ament_index_python import get_package_share_directory

#to import from the same directory:
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import kautham_python_interface as kautham
import xml.etree.ElementTree as ET

from std_msgs.msg import String
from geometry_msgs.msg import Pose
from kautham_interfaces.msg import PathVector
from kautham_interfaces.srv import *
from downward_interfaces.srv import Plan

import pathlib
import random

from collections import defaultdict
import math
import transformations
import pytransform3d.transformations as pt
import pytransform3d.rotations as pr

#Add here any NEW action that can be done
import MOVE, PICK, PLACE, DUMMY, SERVE, FILL
#import TIAGO

#Function to write to xml file in Conf tag
def writePath(taskfile,tex):
    taskfile.write("\t\t<Conf> %s </Conf>\n" % tex)
    return True


#initialising data structure to store scene info
class knowledge:
    def __init__(self):
        self.taskfile=''
        self.graspedobject= False
        self.graspTransfUsed=''
        self.graspControlsUsed=''
        self.directory=''
        self.Robot_move_control= ''

global info
info = knowledge()

class DownwardClient(Node):
    def __init__(self):
        super().__init__('downward_client')
        self.downward_client = self.create_client(Plan, 'downward_service')
        while not self.downward_client.wait_for_service(timeout_sec=1.0):
            print("Service not available, waiting again...")
        self.req = Plan.Request()

    def send_request(self, problem, domain, evaluator, search):
        self.req.problem = problem
        self.req.domain = domain
        self.req.evaluator = evaluator
        self.req.search = search
        self.future = self.downward_client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

#Function to compute grasp config
def computeGraspControls(pose, trygrasp, rob, robotIndex):
    #Check for pose/poseregion
    if len(pose)>7:
        #For Poseregion
        obj_pose=[random.uniform(pose[0], pose[1]), random.uniform(pose[2], pose[3]),pose[4], pose[5],pose[6],pose[7],pose[8]]
    else:
        #For pose
        obj_pose=pose
    Rob_pose= list(kautham.kGetRobotPos(robotIndex))
    #Object wrt to world frame
    q_obj=pr.matrix_from_quaternion([obj_pose[6],obj_pose[3],obj_pose[4],obj_pose[5]])
    P_obj=obj_pose[0:3]
    T_world_object= pt.transform_from(q_obj,P_obj)
    #Use the grasp transf given or compute it with graspIt
    #if trygrasp:
    #    Pose = trygrasp
    #else:
    #    Pose=GraspIt(obj_pose) #call an automatic procedure to compute a grasp
    Pose = trygrasp

    #q_gripper=pr.matrix_from_quaternion(Pose[3:7])#([0.707,0.707,0,0])
    q_gripper=pr.matrix_from_quaternion([Pose[6],Pose[3],Pose[4],Pose[5]])#([0.707,0.707,0,0])
    P_gripper=Pose[0:3]#[-0.165,0,0.06]
    T_object_gripper= pt.transform_from(q_gripper,P_gripper)
    #Robot wrt to world frame
    q_rob=pr.matrix_from_quaternion([Rob_pose[6],Rob_pose[3],Rob_pose[4],Rob_pose[5]])
    P_rob=Rob_pose[0:3]
    T_world_robot= pt.transform_from(q_rob,P_rob)
    #its inverse
    T_robot_world = pt.invert_transform(T_world_robot)

    #Gripper wrt Robot
    #(be carefule with concat - the following is correct)
    T_robot_object= pt.concat(T_world_object,T_robot_world)
    T_robot_gripper= pt.concat(T_object_gripper,T_robot_object)
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    print("T_world_robot ",pt.pq_from_transform(T_world_robot))
    print("T_world_object ",pt.pq_from_transform(T_world_object))
    print("T_robot_object ",pt.pq_from_transform(T_robot_object))
    print("T_object_gripper ",pt.pq_from_transform(T_object_gripper))
    print("T_robot_gripper ",pt.pq_from_transform(T_robot_gripper))
    #convert T_robot_gripper to (pos+quaterion_xyzw)
    Pose_Final_i= pt.pq_from_transform(T_robot_gripper)
    q_pose=pr.quaternion_xyzw_from_wxyz(pr.check_quaternion(Pose_Final_i[3:7]))
    Pose_Final=[Pose_Final_i[0],Pose_Final_i[1],Pose_Final_i[2]]
    Pose_Final.extend(q_pose)
    #round
    Pose_rounded = [ round(elem, 6) for elem in Pose_Final ]
    print("Pose rounded",Pose_rounded)

    #depending on the robot in the task, IK function is called respectively
    called_robot = rob.capitalize() + "_IK"
    #compute IK
    return getattr(globals()[rob.upper()],called_robot)(Pose_rounded) #from TIAGO or YUMI module, call the IK function

def main():
    rclpy.init(args=None)
    node = rclpy.create_node('ktmpb_python_interface')
    node.get_logger().info("Starting Task and Motion Planning Interface Python Client")

    root_demo_folder = get_package_share_directory("ktmpb_interfaces")
    print("root_demo_folder = ", root_demo_folder)

    args = sys.argv[1:] # args is a list of the command line args
    if len(args)==4: #['/demos/OMPL_geo_demos/Table_Rooms_R2/tampconfig_a.xml', '--ros-args', '-r', '__node:=ktmpb_python_interface']
        tampconfig_file = root_demo_folder+args[0]
    else:
        print(args)
        print(len(args))
        print("Erroneous number of args")
        print("Use one arguments to define the tampconfig (see table_rooms_a.launch.py)")
        return

    #Open config file
    config_tree = ET.parse(tampconfig_file)
    config_root = config_tree.getroot()
    #Get data from config file
    #Get data for Problem files
    pddldomainfile=config_root.find('Problemfiles').find('pddldomain').get('name')
    pddlfactsfile=config_root.find('Problemfiles').find('pddlproblem').get('name')
    kauthamproblem = config_root.find('Problemfiles').find('kautham').get('name')
    DIRECTORY =config_root.find('Problemfiles').find('directory').get('name')
    print("Using kautham problem",kauthamproblem)
    print("Using pddl facts file", pddlfactsfile)
    #Get data for states
    Object_pose={}
    Object_kthname={}
    Robot_pose={}
    Robot_control={}

    for val in config_root.find('States').find('Initial').findall('Object'):
        object_name = val.get('name')
        object_kthname = val.get('kthname')
        object_pose= val.text
        object_pose=[float(f) for f in object_pose.split()]
        Object_pose[object_name]= object_pose
        Object_kthname[object_name]= object_kthname
        print("object_name= ",object_name)
        print("object_kthname= ",object_kthname)
        print("object_pose= ",object_pose)

    for val in config_root.find('States').find('Initial').findall('Robot'):
        robot_name= val.get('name')
        robot_controlfile= val.get('controlfile')
        robot_pose= val.text
        robot_pose=[float(f) for f in robot_pose.split()]
        Robot_pose[robot_name]= robot_pose
        Robot_control[robot_name]= robot_controlfile
        print("robot_name= ",robot_name)
        print("robot_pose= ",robot_pose)
        print("robot_controlfile= ",robot_controlfile)

    #BELOW IS ADDED UNTIL 'THE END'
    actions = []
    action_elements = []

    for var in config_root.find('Actions'):
        actions.append(var.tag)
        action_elements.append(var)
    print("Action elements: ", action_elements)

    for action,action_element in zip(actions,action_elements):
        read_action = action + "_read"
        print("Read action: ", read_action)
        print(action.upper())
        sum_attrib=""
        for b in action_element.attrib.values():
            sum_attrib+=b
        final_action=action.upper() + sum_attrib
        print(final_action)
        globals()[final_action] = getattr(globals()[action.upper()], read_action)(action_element)
    #THE END

    # print("pick dict:",pick)
    #Setting problem files
    modelFolder = root_demo_folder + "/demos/models/"
    #global directory
    info.directory = root_demo_folder + DIRECTORY#"/demos/OMPL_geo_demos/Table_Rooms_R2/"

    kauthamProblemFile= info.directory + kauthamproblem
    pddlDomainFile = info.directory + pddldomainfile
    pddlProblemFile = info.directory + pddlfactsfile

    print("kauthamProblemFile = ", kauthamProblemFile)
    print("pddlDomainFile = ", pddlDomainFile)
    print("pddlProblemFile = ", pddlProblemFile)

    #CALLING DOWNWARD TO SOLVE THE TASK PLAN USING FF
    my_downward_client = DownwardClient()

    downward_ros_path = get_package_share_directory("downward_interfaces")

    strProblemFile=open(pddlProblemFile,"r").read()
    print("---------- ProblemFile ------------")
    print(strProblemFile)

    strDomainFile=open(pddlDomainFile,"r").read()
    print("---------- DomainFile -------------")
    print(strDomainFile)

    print("------ CALLING fast-downward as FF -------")
    #evaluator="\"hff=ff()\""
    #search="\"lazy_greedy([hff], preferred=[hff])\""
    #evaluator and search can be left empty for FF since the downward server fills them with the ff info
    evaluator = ""
    search = ""
    r = my_downward_client.send_request(strProblemFile, strDomainFile, evaluator, search)
    if(r.response==True):
        print("Solution plan is: ", r.plan)
    else:
        print("Call to Downward returned FALSE ¿?")
        print(r.plan)
        return
    taskPlan = r.plan
    my_downward_client.destroy_node()
    ### ENDING DOWNWARD CALL

    ##Solving the motion planning problem
    #Open kautham problem
    kautham.kOpenProblem(node, modelFolder,kauthamProblemFile)
    #Set obsctacle from tampconfig file
    for key in Object_pose.keys():
        name = Object_kthname[key]
        kautham.kSetObstaclePos(node, name,Object_pose[key])
    #Set robot from tampconfig file
    #here we're setting the robot initial locations as specified in the config file.
    #there may be several robots and perhaps not all of them involved
    #in solving the task, and here we're placing them
    for key in Robot_pose.keys():
        print(Robot_pose[key])
        kautham.kSetRobControlsNoQuery(node, Robot_control[key])
        kautham.kMoveRobot(node, Robot_pose[key])

    #Save to file
    #global taskfile (name convention is "taskfile_tampconfigname")
    tampconfigname= tampconfig_file.replace(info.directory,'')
    tfile =info.directory+'taskfile_'+tampconfigname
    print("Opening taskfile to write: ",tfile)
    info.taskfile = open(tfile, "w+")
    info.taskfile.write("<?xml version=\"1.0\"?>\n")

    #Write Initial states to config file
    info.taskfile.write("<Task name= \"%s\" >\n" % kauthamproblem)
    info.taskfile.write("\t<Initialstate>\n")
    for keys in Object_pose.keys():
        pos=''
        for j in range(7):
            pos=pos + str(Object_pose[keys][j]) + " "
        #taskfile.write("\t\t<Object object=\"%s\"> %s </Object>\n"%(object_index[keys],pos))
        info.taskfile.write("\t\t<Object object=\"%s\"> %s </Object>\n"%(Object_kthname[keys],pos))
    info.taskfile.write("\t</Initialstate>\n")

    #Loop for each action in the taskPlan to find the paths and (optionally) attach/detach the objects
    for line in taskPlan:
        Line=line.split(" ")
        print("****************************************************************************")
        print(" Processing taskPlan line ", Line)
        print("****************************************************************************")
        try:
            line = line.replace(" ","")
            print(globals()[line])
            function = getattr(globals()[Line[0]], Line[0]) #e.g. MOVE
            arg1 = node
            arg2 = globals()[line] #e.g. move
            arg3 = info
            arg4 = Line
            # print("Function = ", function)
            # print("arg1 = ",line)
            # print("info = ", info)
            # print("Line = ", Line)
            ret = function(arg1, arg2, arg3, arg4)
            # ret = getattr(globals()[Line[0]], Line[0]) (globals()[Line[0].lower()],info,Line)
            print("Action path planning returned:", ret)
            if ret == False:
                print("Action %s has not been defined" % Line[0])
                break
            else:
                print("Action %s has been defined" % Line[0])
        except:
            print("!!!Action %s has not been defined" % Line[0])


    #Close kautham problem
    kautham.kCloseProblem(node)
    #Close and save XML document
    info.taskfile.write("</Task>")
    info.taskfile.close()
    print("Results saved in ", info.taskfile)

    ####
    node.destroy_node()
    rclpy.shutdown()
    return
