###################################################################################
# This is a DUMMY action. It just prints the info encoded in the tampconfig file and
# prints the robot configuration.
#
# To define any NEW action you need to:
#
# 1. Add it to the list of imported actions in the ktmpb_python_interface.py file:
#       import MOVE, PICK, PLACE, DUMMY, MYACTION
#
# 2. Create the MYACTION.py file, like this DUMMY action. 
#    Two functions should be defined:
#
# 2a. Function for the management of the action on the task plan:
#   def MYACTION(node, myaction,info,Line): 
#
# 2b. Function to read the tampconfig file with the parameteres of the action
#   def Myaction_read(action_element): 
#
#3. Define the action in the PDDL domain file, e.g.:
#    (:types obstacle robot location dummyparam)
#    (:action dummy
#     :parameters (?rob - robot ?param1 - dummyparam ?param2 - dummyparam)
#     :precondition (not (dummyCalled ?rob ?param1 ?param2))
#     :effect (dummyCalled ?rob ?param1 ?param2)
#    )
#   like in the manipulation_domain_chess_dummy.pddl file
#
#4. Use it in the PDDL problem file, e.g.
#    (:goal
#        (and (in pawnB1 pos2)
#             (dummyCalled ur3a d1 d2))
#    )
#   like in the manipulation_problem_chess_dummy file


import kautham_python_interface as kautham
import ktmpb_python_interface

import xml.etree.ElementTree as ET
from collections import defaultdict

global dummy
dummy = defaultdict(lambda: defaultdict(dict))

def DUMMY(node, dummy,info,Line): #management of the action on the task plan
    print("**************************************************************************")
    print("  DUMMY ACTION   ")
    print("**************************************************************************")
    
    action=Line[0]
    rob= Line[1]
    parameter1 = Line[2]
    parameter2 = Line[3]

    print(action +" "+rob+" "+parameter1+" "+parameter2)
    try:
        Robot_index=dummy['Rob']
        Robot_control=dummy['Cont']
        dummy_tag_value = dummy['DummyTag']
        dummy_multytag = dummy['DummyMultiEntryTag']
    except:
        print(action +" "+rob+" "+parameter1+" "+parameter2+" Not defined in config file ")

    print("Param1= ", parameter1)
    print("Param2= ", parameter2)
    print("DummyTag=", dummy_tag_value)
    print("DummyMultiEntryTag:")
    for multientrytagname in dummy_multytag.keys():
        dummytag=dummy_multytag[str(multientrytagname)]
        print(multientrytagname,": ",dummytag)

    info.Robot_move_control= Robot_control
    print("Robot control=",Robot_control)
    #Set Robot Control
    kautham.kSetRobControlsNoQuery(node, Robot_control)

    #Get Robot Pos
    robpos = kautham.kGetRobotPos(node, Robot_index)
    print("Robot pos is ", robpos)

    return True

##########################################################################
#Configure here the info that is input through the TAMP configuration file
##########################################################################
#
# In the example of this Dummy action the following info could be written in the tamconfig file:
#
#   <Dummy robot="UR3A" parameter1="D1" parameter2="D2">
#       <Rob> 0 </Rob> <!--Optional, but usually needed if the action involves the robot -->
#       <Cont>controls/ur3_robotniq_1.cntr</Cont> <!--The controls to move the robot if a tag Rob exists -->
#       <DummyTag> Dummy_tag_value </DummyTag> <!-- Enter the tags with the info needed for the action -->
#       <DummyMultiEntryTag multientrytagname = "dummy_1"> 1.0 2.0 3.0 </DummyMultiEntryTag> <!-- Multy entry tags are also possible -->
#       <DummyMultiEntryTag multientrytagname = "dummy_2"> -1.0 -2.0 -3.0 </DummyMultiEntryTag> <!-- Multy entry tags are also possible -->
#   </Dummy>
#
#  
def Dummy_read(action_element): #reading from the tamp configuration file
    for val in action_element.attrib:
        globals()[val] = action_element.attrib[val]

    dummy = {} #stores all the info red from the tamconfig file related to the Dummy action
               # This info can then be accessed, e.g. the info in the DummyTag: dummy['DummyTag']
    dummy_multientry = {} #optional-to be used if multientry tags are defined
                # dummy_multytag = dummy['DummyMultiEntryTag']
                # for multientrytagname in dummy_multytag.keys():
                #   dummytag=dummy_multytag[str(multientrytagname)]

    for el in action_element:
        try:
            globals()[el.tag] = int(el.text)
        except:
            try:
                globals()[el.tag] = [float(f) for f in str(el.text).strip().split()]
            except:
                globals()[el.tag] = str(el.text).strip()
        #if the action does not have any multientry tag then this "if" can be eliminated
        if el.tag == 'DummyMultiEntryTag': #variables with multiple entries should be added the same way
            tag_name = el.get('multientrytagname')
            tag_entry= el.text
            tag_entry=[float(f) for f in tag_entry.split()]
            dummy_multientry[tag_name]= tag_entry
            globals()[el.tag] = dummy_multientry

        dummy.update({el.tag : globals()[el.tag]})

    return dummy
