#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from ktmpb.srv import TiagoIk

def TiagoJointAngleToKauthamControl (pose):
    Pose=[]
    Pose.append((pose[0]+0)/0.35) #torso_lift
    Pose.append((pose[1]-0.02)/(-0.02+2.728893571890)) #arm_1
    Pose.append((pose[2]+1.55079632679)/(1.55079632679+1.0708307825)) #arm_2
    Pose.append((pose[3]+3.51429173529)/(3.51429173529+1.55079632679)) #arm_3
    Pose.append((pose[4]+0.372699081699)/(0.372699081699+2.33619449019)) #arm_4
    Pose.append((pose[5]+2.07439510239)/(2.07439510239+2.07439510239)) #arm_5
    Pose.append((pose[6]+1.39371669412)/(1.39371669412+1.39371669412)) #arm_6
    Pose.append((pose[7]+2.07439510239)/(2.07439510239+2.07439510239)) #arm_7
    Pose.append(pose[8])#gripper

    print("IK CONTROLS SOLUTION......................")
    print(Pose)
    return Pose

#Function to call Tiago Ik service to get configuration of Tiago (In joint angles in radian)
def Tiago_IK(node, pose):
    tiagoik_client = node.create_client(TiagoIk, '/tiago_Ik')

    req = TiagoIk.Request()
    print(pose)
    req.pose = pose

    while not tiagoik_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('TiagoIk service not available, waiting again...')
    future=tiagoik_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    r = future.result()

    if list(r.Conf)==[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]:
        print('Failed to compute Inverse Kinematics for the given position')
        return False
    conf=list(r.Conf)
    print("IK SOLUTION......................")
    print(conf)
    return TiagoJointAngleToKauthamControl(conf)

    