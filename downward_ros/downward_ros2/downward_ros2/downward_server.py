#!/usr/bin/env python3

from __future__ import print_function

import rclpy
from rclpy.node import Node
from downward_interfaces.srv import Plan
import os
from os.path import exists

class DownwardServer(Node):
    
    def __init__(self):
        super().__init__('downward_server')
        self.srv = self.create_service(Plan, 'downward_service', self.downward_plan)

    #Service to call Fast-downward 
    # by default FF is used
    def downward_plan(self, req, res):
        print("\n================================")
        print("====STARTING downward planner===")
        print("================================")
        print("PDDL problem file ",req.problem)
        print("PDDL domain file ",req.domain)
        if(req.evaluator=="" and req.search=="" ):
            # print("------ CALLING fast-downward as FF -------")
            # evaluator = "\"hff=ff()\""
            # search = "\"lazy_greedy([hff], preferred=[hff])\""
            print("------ CALLING the landmark heuristic combined with goal-counting within a lazy weighted A* search strategy. -------")
            evaluator = "\"lmcut=lmcut()\""
            search = "\"lazy_wastar([lmcut], w=2, reopen_closed=true)\""
        else:
            evaluator = req.evaluator
            search = req.search
        print("evaluator used ",evaluator)
        print("search used ",search)

        f = open("problemfile", "w")
        f.write(req.problem)
        f.close()
        f = open("domainfile.pddl", "w")
        f.write(req.domain)
        f.close()

        command="fast-downward domainfile.pddl problemfile --evaluator " + evaluator + " --search " + search 
    
        if(exists("./sas_plan")):
            print("sas_plan exists - I will delete it")
            os.system("rm sas_plan") #remove previous plan, if any
        #call downward
        os.system(command)
        #check sas_plan has been obtained, otherwise report error
        if(not exists("./sas_plan")):
            print("Downward has not been able to generate sas_plan")
            res.plan = ["dummy"]
            res.response = False
            return res

        f = open("sas_plan","r")
        lines = f.readlines()

        solution = []
        print("--- PLAN ---")
        for i in range(len(lines)-1):
            solution.append(lines[i].lstrip("(").rstrip(")\n").upper())#return as uppercase since this was what the FF package did...
            print(solution[i])
        
        res.plan = solution #solution=["action1","action2"]
        res.response = True
        return res

def main():
    rclpy.init()
    downward_server = DownwardServer()
    print("Downward server initialized!")
    rclpy.spin(downward_server)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
