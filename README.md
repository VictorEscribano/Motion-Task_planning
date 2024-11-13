# Task_and_motion_planning2
![Screenshot from 2024-11-13 18-27-56](https://github.com/user-attachments/assets/d37b85ad-c548-4f75-8043-789c6562659e)

This meta-repository contains:

- module **downward_ros**: package that wraps the Fast-Downward set of task planners - (using **ros2** branch)

- module **kautham_interfaces**: package that wraps the calls to the Kautham services

- module **ktmpb**: package that uses the Fast-Downward and Katham services to plan at task and motion levels - (using **ros2** branch)

## Clone and build
```
$ mkdir -p colcon_ws/src
$ cd colcon_ws/src
$ git clone  https://github.com/VictorEscribano/Motion-Task_planning.git
$ cd ..
$ colcon build
```

## Test
The **ktmpb** package has a demo folder called *task_and_motion_planning2/ktmpb/ktmpb_interfaces/demos/* that is installed in *install/ktmpb_interfaces/share/ktmpb_interfaces/demos/*.

To test the task and motion planning client launch the following file:

```
$ ros2 launch ktmpb_client table_rooms_a.launch.py
```

This example uses the task and motion planning configuration file **tampconfig_a.xml** in the folder *demos/OMPL_geo_demos/Table_Rooms_R2*, where the following PDDL files and Kautham files to be used are defined:

    - pddldomain file: "ff-domains/manipulationdomain.pddl"
    - pddlproblem file "ff-domains/manipulation_problem_A"
    - kautham file: "OMPL_RRTconnect_table_rooms_R2_a.xml"

The resulting file (in the folder *install/ktmpb_interfaces/share/ktmpb_interfaces/demos/*) is called:

    - taskfile_tampconfig_a.xml

Open the *OMPL_RRTconnect_table_rooms_R2_a.xml* prioblem using the Kautham GUI and then load and run the taskfile.
