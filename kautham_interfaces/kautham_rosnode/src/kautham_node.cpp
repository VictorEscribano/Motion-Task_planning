/*************************************************************************\
   Copyright 2014 Institute of Industrial and Control Engineering (IOC)
                 Universitat Politecnica de Catalunya
                 BarcelonaTech
    All Rights Reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the
    Free Software Foundation, Inc.,
    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 \*************************************************************************/

/* Author: Pol Ramon, Jan Rosell*/

#include <rclcpp/rclcpp.hpp>
#include <kautham/kauthamshell.h>

#include <memory>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

// Messages:
#include <std_msgs/msg/string.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp>
//#include <sensor_msgs/JointState.h>
//#include <tf2_ros/static_transform_broadcaster.h>

// Services:
#include "kautham_interfaces/srv/close_problem.hpp"
#include "kautham_interfaces/srv/obs_pos.hpp"
#include "kautham_interfaces/srv/open_problem.hpp"
#include "kautham_interfaces/srv/problem_opened.hpp"
#include "kautham_interfaces/srv/remove_robot.hpp"
#include "kautham_interfaces/srv/rob_pos.hpp"
#include "kautham_interfaces/srv/set_rob_controls_no_query.hpp"
#include "kautham_interfaces/srv/set_robots_config.hpp"
#include "kautham_interfaces/srv/path_dof_names.hpp"
#include "kautham_interfaces/srv/get_path.hpp"
#include "kautham_interfaces/srv/set_query.hpp"
#include "kautham_interfaces/srv/attach_obstacle2_robot_link.hpp"
#include "kautham_interfaces/srv/detach_obstacle.hpp"
#include "kautham_interfaces/srv/check_collision.hpp"
#include "kautham_interfaces/srv/set_planner_parameter.hpp"
#include "kautham_interfaces/srv/set_planner_by_name.hpp"

/*
#include <kautham/OpenProblemStream.h>
#include <kautham/CheckCollision.h>
#include <kautham/SetRobotsConfig.h>
#include <kautham/SetObstaclesConfig.h>
#include <kautham/SetQuery.h>
#include <kautham/SetInit.h>
#include <kautham/SetGoal.h>
#include <kautham/SetInitObs.h>
#include <kautham/ClearSampleSet.h>
#include <kautham/SetRobControls.h>
#include <kautham/SetRobControlsNoQuery.h>
#include <kautham/SetRobControlsStream.h>
#include <kautham/SetDefaultRobControls.h>
#include <kautham/SetObsControls.h>
#include <kautham/SetObsControlsStream.h>
#include <kautham/SetFixedObsControls.h>
#include <kautham/SetPlannerByName.h>
#include <kautham/SetPlanner.h>
#include <kautham/SetPlannerStream.h>
#include <kautham/SetPlannerParameter.h>
#include <kautham/Solve.h>
#include <kautham/GetPath.h>
#include <kautham/AddRobot.h>
#include <kautham/RemoveRobot.h>
#include <kautham/AddObstacle.h>
#include <kautham/RemoveObstacle.h>
#include <kautham/AttachObstacle2RobotLink.h>
#include <kautham/DetachObstacle.h>
#include <kautham/Connect.h>
#include <kautham/GetLastPlanComputationTime.h>
#include <kautham/GetNumEdges.h>
#include <kautham/GetNumVertices.h>
#include <kautham/ObsPos.h>
#include <kautham/RobPos.h>
#include <kautham/FindIK.h>
#include <kautham/LoadRobots.h>
#include <kautham/LoadObstacles.h>
#include <kautham/VisualizeScene.h>
#include <kautham/robconf.h>
#include <kautham/GetObstaclesNames.h>
#include <kautham/PathDofNames.h>
*/

using namespace std;
using namespace Kautham;

kauthamshell* ksh;

class KauthamServer : public rclcpp::Node
{
public:
    // Constructor:
    KauthamServer() : Node("kautham_node"){
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Starting Kautham_Service");
        
        // Servers constructors:
        closeProblem_server_ = this->create_service<kautham_interfaces::srv::CloseProblem>("kautham_node/CloseProblem", std::bind(&KauthamServer::srvCloseProblem, this,std::placeholders::_1, std::placeholders::_2));
        problemOpened_server_ = this->create_service<kautham_interfaces::srv::ProblemOpened>("kautham_node/ProblemOpened", std::bind(&KauthamServer::srvProblemOpened, this,std::placeholders::_1, std::placeholders::_2));
        openProblem_server_ = this->create_service<kautham_interfaces::srv::OpenProblem>("kautham_node/OpenProblem", std::bind(&KauthamServer::srvOpenProblem, this,std::placeholders::_1, std::placeholders::_2));
        setRobControlsNoQuery_server_ = this->create_service<kautham_interfaces::srv::SetRobControlsNoQuery>("kautham_node/SetRobControlsNoQuery", std::bind(&KauthamServer::srvSetRobControlsNoQuery, this,std::placeholders::_1, std::placeholders::_2));
        setObstaclePos_server_ = this->create_service<kautham_interfaces::srv::ObsPos>("kautham_node/SetObstaclePos", std::bind(&KauthamServer::srvSetObstaclePos, this,std::placeholders::_1, std::placeholders::_2));
        getObstaclePos_server_ = this->create_service<kautham_interfaces::srv::ObsPos>("kautham_node/GetObstaclePos", std::bind(&KauthamServer::srvGetObstaclePos, this,std::placeholders::_1, std::placeholders::_2));
        removeRobot_server_ = this->create_service<kautham_interfaces::srv::RemoveRobot>("kautham_node/RemoveRobot", std::bind(&KauthamServer::srvRemoveRobot, this,std::placeholders::_1, std::placeholders::_2));
        setRobotsConfig_server_ = this->create_service<kautham_interfaces::srv::SetRobotsConfig>("kautham_node/SetRobotsConfig", std::bind(&KauthamServer::srvSetRobotsConfig, this,std::placeholders::_1, std::placeholders::_2));
        pathDofNames_server_ =  this->create_service<kautham_interfaces::srv::PathDofNames>("kautham_node/PathDofNames", std::bind(&KauthamServer::srvPathDofNames, this,std::placeholders::_1, std::placeholders::_2));
        getRobPos_server_ =  this->create_service<kautham_interfaces::srv::RobPos>("kautham_node/GetRobotPos", std::bind(&KauthamServer::srvGetRobotPos, this,std::placeholders::_1, std::placeholders::_2));
        getPath_server_ =  this->create_service<kautham_interfaces::srv::GetPath>("kautham_node/GetPath", std::bind(&KauthamServer::srvGetPath, this,std::placeholders::_1, std::placeholders::_2));
        setQuery_server_ =  this->create_service<kautham_interfaces::srv::SetQuery>("kautham_node/SetQuery", std::bind(&KauthamServer::srvSetQuery, this,std::placeholders::_1, std::placeholders::_2));
        detachObstacle_server_ =  this->create_service<kautham_interfaces::srv::DetachObstacle>("kautham_node/DetachObstacle", std::bind(&KauthamServer::srvDetachObstacle, this,std::placeholders::_1, std::placeholders::_2));
        attachObstacle2RobotLink_server_ =  this->create_service<kautham_interfaces::srv::AttachObstacle2RobotLink>("kautham_node/AttachObstacle2RobotLink", std::bind(&KauthamServer::srvAttachObstacle2RobotLink, this,std::placeholders::_1, std::placeholders::_2));
        checkCollision_server_ =  this->create_service<kautham_interfaces::srv::CheckCollision>("kautham_node/CheckCollision", std::bind(&KauthamServer::srvCheckCollision, this,std::placeholders::_1, std::placeholders::_2));
        setplannerparameter_server_ =  this->create_service<kautham_interfaces::srv::SetPlannerParameter>("kautham_node/SetPlannerParameter", std::bind(&KauthamServer::srvSetPlannerParameter, this,std::placeholders::_1, std::placeholders::_2));
        setplannerbyname_server_ =  this->create_service<kautham_interfaces::srv::SetPlannerByName>("kautham_node/SetPlannerByName", std::bind(&KauthamServer::srvSetPlannerByName, this,std::placeholders::_1, std::placeholders::_2));
    }

    // Callbacks definitions:
    bool srvCloseProblem(const std::shared_ptr<kautham_interfaces::srv::CloseProblem::Request> req, std::shared_ptr<kautham_interfaces::srv::CloseProblem::Response> res);
    bool srvProblemOpened(const std::shared_ptr<kautham_interfaces::srv::ProblemOpened::Request> req, std::shared_ptr<kautham_interfaces::srv::ProblemOpened::Response> res);
    bool srvOpenProblem(const std::shared_ptr<kautham_interfaces::srv::OpenProblem::Request> req, std::shared_ptr<kautham_interfaces::srv::OpenProblem::Response> res);
    bool srvSetRobControlsNoQuery(const std::shared_ptr<kautham_interfaces::srv::SetRobControlsNoQuery::Request> req, std::shared_ptr<kautham_interfaces::srv::SetRobControlsNoQuery::Response> res);
    bool srvSetObstaclePos(const std::shared_ptr<kautham_interfaces::srv::ObsPos::Request> req, std::shared_ptr<kautham_interfaces::srv::ObsPos::Response> res);
    bool srvGetObstaclePos(const std::shared_ptr<kautham_interfaces::srv::ObsPos::Request> req, std::shared_ptr<kautham_interfaces::srv::ObsPos::Response> res);
    bool srvRemoveRobot(const std::shared_ptr<kautham_interfaces::srv::RemoveRobot::Request> req, std::shared_ptr<kautham_interfaces::srv::RemoveRobot::Response> res);
    bool srvSetRobotsConfig(const std::shared_ptr<kautham_interfaces::srv::SetRobotsConfig::Request> req, std::shared_ptr<kautham_interfaces::srv::SetRobotsConfig::Response> res);
    bool srvPathDofNames(const std::shared_ptr<kautham_interfaces::srv::PathDofNames::Request> req, std::shared_ptr<kautham_interfaces::srv::PathDofNames::Response> res);
    bool srvGetRobotPos(const std::shared_ptr<kautham_interfaces::srv::RobPos::Request> req, std::shared_ptr<kautham_interfaces::srv::RobPos::Response> res);
    bool srvGetPath(const std::shared_ptr<kautham_interfaces::srv::GetPath::Request> req, std::shared_ptr<kautham_interfaces::srv::GetPath::Response> res);
    bool srvSetQuery(const std::shared_ptr<kautham_interfaces::srv::SetQuery::Request> req, std::shared_ptr<kautham_interfaces::srv::SetQuery::Response> res);
    bool srvDetachObstacle(const std::shared_ptr<kautham_interfaces::srv::DetachObstacle::Request> req, std::shared_ptr<kautham_interfaces::srv::DetachObstacle::Response> res);
    bool srvAttachObstacle2RobotLink(const std::shared_ptr<kautham_interfaces::srv::AttachObstacle2RobotLink::Request> req, std::shared_ptr<kautham_interfaces::srv::AttachObstacle2RobotLink::Response> res);
    bool srvCheckCollision(const std::shared_ptr<kautham_interfaces::srv::CheckCollision::Request> req, std::shared_ptr<kautham_interfaces::srv::CheckCollision::Response> res);
    bool srvSetPlannerParameter(const std::shared_ptr<kautham_interfaces::srv::SetPlannerParameter::Request> req, std::shared_ptr<kautham_interfaces::srv::SetPlannerParameter::Response> res);
    bool srvSetPlannerByName(const std::shared_ptr<kautham_interfaces::srv::SetPlannerByName::Request> req, std::shared_ptr<kautham_interfaces::srv::SetPlannerByName::Response> res);
    

private:

    // Variables:
    bool visualizescene = false;

    //Messages:
    std_msgs::msg::String my_msg;
    // geometry_msgs::msg::transform_stamped

    // Servers objects:
    rclcpp::Service<kautham_interfaces::srv::CloseProblem>::SharedPtr closeProblem_server_;
    rclcpp::Service<kautham_interfaces::srv::ProblemOpened>::SharedPtr problemOpened_server_;
    rclcpp::Service<kautham_interfaces::srv::OpenProblem>::SharedPtr openProblem_server_;
    rclcpp::Service<kautham_interfaces::srv::SetRobControlsNoQuery>::SharedPtr setRobControlsNoQuery_server_;
    rclcpp::Service<kautham_interfaces::srv::ObsPos>::SharedPtr setObstaclePos_server_;
    rclcpp::Service<kautham_interfaces::srv::ObsPos>::SharedPtr getObstaclePos_server_;
    rclcpp::Service<kautham_interfaces::srv::RemoveRobot>::SharedPtr removeRobot_server_;
    rclcpp::Service<kautham_interfaces::srv::SetRobotsConfig>::SharedPtr setRobotsConfig_server_;
    rclcpp::Service<kautham_interfaces::srv::PathDofNames>::SharedPtr pathDofNames_server_;
    rclcpp::Service<kautham_interfaces::srv::RobPos>::SharedPtr getRobPos_server_;
    rclcpp::Service<kautham_interfaces::srv::GetPath>::SharedPtr getPath_server_;
    rclcpp::Service<kautham_interfaces::srv::SetQuery>::SharedPtr setQuery_server_;
    rclcpp::Service<kautham_interfaces::srv::DetachObstacle>::SharedPtr detachObstacle_server_;
    rclcpp::Service<kautham_interfaces::srv::AttachObstacle2RobotLink>::SharedPtr attachObstacle2RobotLink_server_;
    rclcpp::Service<kautham_interfaces::srv::CheckCollision>::SharedPtr checkCollision_server_;
    rclcpp::Service<kautham_interfaces::srv::SetPlannerParameter>::SharedPtr setplannerparameter_server_;
    rclcpp::Service<kautham_interfaces::srv::SetPlannerByName>::SharedPtr setplannerbyname_server_;
};

// Callbacks code:
bool KauthamServer::srvCloseProblem(const std::shared_ptr<kautham_interfaces::srv::CloseProblem::Request> req, std::shared_ptr<kautham_interfaces::srv::CloseProblem::Response> res){
    (void) req;//unused
    (void) res;//unused
    
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "++++++++  closeProblem ++++++++++\n");
    ksh->closeProblem();

    return true;
}

bool KauthamServer::srvProblemOpened(const std::shared_ptr<kautham_interfaces::srv::ProblemOpened::Request> req, std::shared_ptr<kautham_interfaces::srv::ProblemOpened::Response> res){
    (void) req;//unused
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "++++++++  problemOpened ++++++++++\n");

    res->response = ksh->problemOpened();

    return true;
}

bool KauthamServer::srvOpenProblem(const std::shared_ptr<kautham_interfaces::srv::OpenProblem::Request> req, std::shared_ptr<kautham_interfaces::srv::OpenProblem::Response> res){
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Opening problem:: %s", req->problem.c_str());
    
    string dir = req->problem;
    dir.erase(dir.find_last_of("/") + 1, dir.length());
    string absPath = dir;
    vector <string> def_path =req->dir;

    def_path.push_back(dir);
    def_path.push_back(dir+"/../../models/");
    dir = absPath.substr(0,absPath.find_last_of("/")+1);
    def_path.push_back(dir);
    def_path.push_back(dir+"/../../models/");

    if (ksh->openProblem(req->problem, def_path)) {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "The problem file has been opened successfully.\n");
        my_msg.data = "The problem file has been opened successfully.";
        res->response = true;
    } else {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "The problem file couldn't be opened.\n");
        my_msg.data = "The problem file couldn't be opened.";
        res->response = false;
    }
    
    //res->response = true;

    return true;
}

bool KauthamServer::srvSetRobControlsNoQuery(const std::shared_ptr<kautham_interfaces::srv::SetRobControlsNoQuery::Request> req, std::shared_ptr<kautham_interfaces::srv::SetRobControlsNoQuery::Response> res){
    res->response = ksh->setRobControlsNoQuery(req->controls);

    return true;
}

bool KauthamServer::srvSetObstaclePos(const std::shared_ptr<kautham_interfaces::srv::ObsPos::Request> req, std::shared_ptr<kautham_interfaces::srv::ObsPos::Response> res){
    res->response = ksh->setObstaclePos(req->obsname, req->setpos);

    // if(this->visualizescene)
    // {
    //     std::map<std::string, geometry_msgs::TransformStamped>::iterator it = otransform.find(req->obsname);
    //     it->second.header.stamp = ros::Time::now();
    //     it->second.header.frame_id = "world";
    //     std::stringstream my_child_frame_id;
    //     my_child_frame_id  << "obstacle_"<<req->obsname<<"_base";
    //     it->second.child_frame_id = my_child_frame_id.str();
    //     std::vector<float> pose;
    //     pose.resize(7);
    //     pose[0] = req->set_pos.at(0);
    //     pose[1] = req->set_pos.at(1);
    //     pose[2] = req->set_pos.at(2);
    //     pose[3] = req->set_pos.at(3);
    //     pose[4] = req->set_pos.at(4);
    //     pose[5] = req->set_pos.at(5);
    //     pose[6] = req->set_pos.at(6);
    //     SE3Conf::fromAxisToQuaternion(pose);
    //     it->second.transform.translation.x = pose[0];
    //     it->second.transform.translation.y = pose[1];
    //     it->second.transform.translation.z = pose[2];
    //     it->second.transform.rotation.x = pose[3];
    //     it->second.transform.rotation.y = pose[4];
    //     it->second.transform.rotation.z = pose[5];
    //     it->second.transform.rotation.w = pose[6];
    // }
    return true;
}

bool KauthamServer::srvGetObstaclePos(const std::shared_ptr<kautham_interfaces::srv::ObsPos::Request> req, std::shared_ptr<kautham_interfaces::srv::ObsPos::Response> res)
{
    std::vector<float> obsPos;
    res->response = ksh->getObstaclePos(req->obsname, obsPos);
    if(res->response) {
        res->getpos = obsPos;
    }
    return true;
}

bool KauthamServer::srvRemoveRobot(const std::shared_ptr<kautham_interfaces::srv::RemoveRobot::Request> req, std::shared_ptr<kautham_interfaces::srv::RemoveRobot::Response> res){
    res->response = ksh->removeRobot(req->index);

    return true;
}

bool KauthamServer::srvSetRobotsConfig(const std::shared_ptr<kautham_interfaces::srv::SetRobotsConfig::Request> req, std::shared_ptr<kautham_interfaces::srv::SetRobotsConfig::Response> res){
        
    std::vector<RobConf> config;
    bool setRC = ksh->setRobotsConfig(req->controls, config);
    res->config.resize(config.size());
    for(unsigned int i=0; i<config.size();i++)
    {
        //fill the response
        res->config[i].base.position.x = config[i].first.getPos().at(0);
        res->config[i].base.position.y = config[i].first.getPos().at(1);
        res->config[i].base.position.z = config[i].first.getPos().at(2);
        res->config[i].base.orientation.x = config[i].first.getOrient().at(0);
        res->config[i].base.orientation.y = config[i].first.getOrient().at(1);
        res->config[i].base.orientation.z = config[i].first.getOrient().at(2);
        res->config[i].base.orientation.w = config[i].first.getOrient().at(3);
        res->config[i].joints = config[i].second.getCoordinates();

        // if(visualizescene)
        // {
        //     //update the broadcasted transforms for the base
        //     rtransform[i].header.stamp = ros::Time::now();
        //     rtransform[i].header.frame_id = "world";
        //     std::stringstream my_child_frame_id;
        //     my_child_frame_id  << "robot"<<i<<"_base_link";
        //     rtransform[i].child_frame_id = my_child_frame_id.str();
        //     rtransform[i].transform.translation.x = config[i].first.getPos().at(0);
        //     rtransform[i].transform.translation.y = config[i].first.getPos().at(1);
        //     rtransform[i].transform.translation.z = config[i].first.getPos().at(2);
        //     rtransform[i].transform.rotation.x = config[i].first.getOrient().at(0);
        //     rtransform[i].transform.rotation.y = config[i].first.getOrient().at(1);
        //     rtransform[i].transform.rotation.z = config[i].first.getOrient().at(2);
        //     rtransform[i].transform.rotation.w = config[i].first.getOrient().at(3);

        //     //fill the joint values to be published
        //     if(!guisliders)
        //     {
        //         for(unsigned int j=0; j<joint_state_robot[i].position.size();j++)
        //             joint_state_robot[i].position[j] = config[i].second.getCoordinates().at(j);
        //     }
        // }
        std::cout<<"ROBOT "<<i<<std::endl;
        std::cout<<"x = "<<res->config[i].base.position.x<<std::endl;
        std::cout<<"y = "<<res->config[i].base.position.y<<std::endl;
        std::cout<<"z = "<<res->config[i].base.position.z<<std::endl;
        std::cout<<"qx = "<<res->config[i].base.orientation.x<<std::endl;
        std::cout<<"qy = "<<res->config[i].base.orientation.y<<std::endl;
        std::cout<<"qz = "<<res->config[i].base.orientation.y<<std::endl;
        std::cout<<"qw = "<<res->config[i].base.orientation.w<<std::endl;
        //std::cout<<"q = (";
        //std::cout<<"ROBOT "<<i<<std::endl;
        //for(unsigned int j=0; j<joint_state_robot[i].position.size();j++)
        //    std::cout<<res.config[i].joints[j]<<" ";
        //std::cout<<std::endl;
        //std::cout<<"ROBOT "<<i<<std::endl;
    }
    res->response = setRC;
    return setRC;
}

//this service returns the names of the dof in the path returned by GetPath
//e.g. for the Tiago we have that each configuration of the path has 23 values according to:
//dofnames =  ['x', 'y', 'z', 'qx', 'qy', 'qz', 'qw', 'wheel_right_joint', 'wheel_left_joint', 'torso_fixed_joint', 'torso_lift_joint', 'head_1_joint', 'head_2_joint', 'arm_1_joint', 'arm_2_joint', 'arm_3_joint', 'arm_4_joint', 'arm_5_joint', 'arm_6_joint', 'arm_7_joint', 'gripper_joint', 'gripper_right_finger_joint', 'gripper_left_finger_joint']
bool KauthamServer::srvPathDofNames(const std::shared_ptr<kautham_interfaces::srv::PathDofNames::Request> req, std::shared_ptr<kautham_interfaces::srv::PathDofNames::Response> res)
{
    (void) req;//unused

    std::vector< std::vector<std::string> > jnames;
    jnames.resize( ksh->getNumRobots() );
    for(unsigned int i = 0; i < ksh->getNumRobots(); i++) {
      if(ksh->getRobotIsSE3enabled(i))
      {
        res->dofnames.push_back("x");
        res->dofnames.push_back("y");
        res->dofnames.push_back("z");
        res->dofnames.push_back("qx");
        res->dofnames.push_back("qy");
        res->dofnames.push_back("qz");
        res->dofnames.push_back("qw");
      }
      ksh->getRobotJointNames(i,jnames[i]);
      for(unsigned int j=0;j<jnames[i].size();j++)
        res->dofnames.push_back(jnames[i][j]);
    }
    return true;
}

bool KauthamServer::srvGetRobotPos(const std::shared_ptr<kautham_interfaces::srv::RobPos::Request> req, std::shared_ptr<kautham_interfaces::srv::RobPos::Response> res)
{
    std::cout<<"srvGetRobotPos service ***********"<<std::endl;
    std::vector<float> robPos;
    res->response = ksh->getRobPos(req->index, robPos);
    if(res->response) {
        for(int i=0; i<robPos.size();i++)
            res->getpos.push_back(robPos[i]);
        std::cout<<"ROBOT size="<<robPos.size()<<" x="<<robPos[0]<<std::endl;
        //res->set__getpos(robPos);
    }

    return true;
}

bool KauthamServer::srvGetPath(const std::shared_ptr<kautham_interfaces::srv::GetPath::Request> req, std::shared_ptr<kautham_interfaces::srv::GetPath::Response> res)
{
    (void) req;//unused
    ostringstream oss;
    if (ksh->getPath(oss)) {
        vector < vector < float > > path;
        istringstream iss(oss.str());
        for (string str; getline(iss,str); ) {
            vector < float > conf;
            std::istringstream strs(str);
            int chars_to_read = strs.str().size();
            while (chars_to_read > 0) {
                getline(strs,str,' ');
                if (str.size() > 0) {
                    conf.push_back(atof(str.c_str()));
                }
                chars_to_read -= str.size() + 1;
            }
            if(conf.size()) path.push_back(conf);
        }
        res->response.resize(path.size());
        for (unsigned int i = 0; i < path.size(); ++i) {
            res->response[i].v.resize(path.at(i).size());
            for (unsigned int j = 0; j < path.at(i).size(); ++j) {
                res->response[i].v[j] = path.at(i).at(j);
            }
        }
        /*
        if(visualizescene)
        {
            ros::Rate rate(2.0);
            //std::cout<<"START visualizescene"<<std::endl;
            for(unsigned int i=0; i<path.size();i++)
            {
              std::cout<<"path step "<<i<<std::endl;
              int indexdof=0;
              for(unsigned int j=0; j<ksh->getNumRobots();j++)
              {
                ros::spinOnce();

                //SE3 part
                if(ksh->getRobotIsSE3enabled(j))
                {
                  //update the broadcasted transforms for the base
                  rtransform[j].header.stamp = ros::Time::now();
                  rtransform[j].header.frame_id = "world";
                  std::stringstream my_child_frame_id;
                  my_child_frame_id  << "robot"<<j<<"_base_link";
                  rtransform[j].child_frame_id = my_child_frame_id.str();
                  rtransform[j].transform.translation.x = path.at(i).at(indexdof++);
                  rtransform[j].transform.translation.y = path.at(i).at(indexdof++);
                  rtransform[j].transform.translation.z = path.at(i).at(indexdof++);
                  rtransform[j].transform.rotation.x = path.at(i).at(indexdof++);
                  rtransform[j].transform.rotation.y = path.at(i).at(indexdof++);
                  rtransform[j].transform.rotation.z = path.at(i).at(indexdof++);
                  rtransform[j].transform.rotation.w = path.at(i).at(indexdof++);
                  //publish robot transform
                  br->sendTransform(rtransform[j]);
                }
                //Rn part
                if(joint_state_robot[j].position.size())
                {
                  //fill the joint values to be published
                  for(unsigned int k=0; k<joint_state_robot[j].position.size();k++)
                  {
                    joint_state_robot[j].position[k] = path.at(i).at(indexdof++);
                  }
                  //publish robot joints
                  joint_state_robot[j].header.stamp = ros::Time::now();
                  joints_publishers[j]->publish(joint_state_robot[j]);
                 }
               }
               //Wait until it's time for another iteration
               rate.sleep();
            }
            //std::cout<<"END visualizescene "<<std::endl;
        }
        */
    }

    return true;
}

bool KauthamServer::srvSetQuery(const std::shared_ptr<kautham_interfaces::srv::SetQuery::Request> req, std::shared_ptr<kautham_interfaces::srv::SetQuery::Response> res)
{
    res->response = ksh->setQuery(req->init,req->goal);

    return true;
}

bool KauthamServer::srvDetachObstacle(const std::shared_ptr<kautham_interfaces::srv::DetachObstacle::Request> req, std::shared_ptr<kautham_interfaces::srv::DetachObstacle::Response> res)
{
    res->response = ksh->detachObstacle(req->obsname);

    return true;
}

bool KauthamServer::srvAttachObstacle2RobotLink(const std::shared_ptr<kautham_interfaces::srv::AttachObstacle2RobotLink::Request> req, std::shared_ptr<kautham_interfaces::srv::AttachObstacle2RobotLink::Response> res)
{
    res->response = ksh->attachObstacle2RobotLink(req->robot,req->link,req->obs);

    return true;
}

bool KauthamServer::srvCheckCollision(const std::shared_ptr<kautham_interfaces::srv::CheckCollision::Request> req, std::shared_ptr<kautham_interfaces::srv::CheckCollision::Response> res)
{
    for (unsigned int i = 0; i < req->config.size(); ++i) {
        cout << req->config.at(i) << " ";
    }
    cout << endl;
    std::pair< std::pair<int, string> , std::pair<int,int> > colliding_elements;
    bool collisionfree;
    string msg;
    res->response = ksh->checkCollision(req->config,&collisionfree, &msg, &colliding_elements);
    res->collisionfree = res->response&&collisionfree;
    res->collidingrob = colliding_elements.first.first;
    res->collidedobs = colliding_elements.first.second;
    res->msg = msg;
    return true;
}

bool KauthamServer::srvSetPlannerParameter(const std::shared_ptr<kautham_interfaces::srv::SetPlannerParameter::Request> req, std::shared_ptr<kautham_interfaces::srv::SetPlannerParameter::Response> res)
{
    res->response = ksh->setPlannerParameter(req->parameter,req->value);

    return true;
}

bool KauthamServer::srvSetPlannerByName(const std::shared_ptr<kautham_interfaces::srv::SetPlannerByName::Request> req, std::shared_ptr<kautham_interfaces::srv::SetPlannerByName::Response> res)
{
    res->response = ksh->setPlannerByName(req->name);

    return true;
}

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    ksh = new kauthamshell();
    rclcpp::spin(std::make_shared<KauthamServer>());
    rclcpp::shutdown();
    return 0;
}
