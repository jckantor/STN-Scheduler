# STN Scheduler

The State-Task Network (STN) is a method for modeling and scheduling multipurpose batch processes developed by Kondili, et al., in 1993, and extended by others. 

This repository consists of a python module STN to assist in the modeling and scheduling of State Task Networks, and Jupyter notebooks demonstrating their use. 

* [Overview of STN Scheduler (to be finished)](http://nbviewer.jupyter.org/github/jckantor/STN-Scheduler/blob/master/notebooks/0_Overview.ipynb)
* [State Task Network Example of Kondili, et. al, 1993](http://nbviewer.jupyter.org/github/jckantor/STN-Scheduler/blob/master/notebooks/1_Kondili_State_Task_Network.ipynb).
* [State Task Network Example of Chu, et. al, 2013](http://nbviewer.jupyter.org/github/jckantor/STN-Scheduler/blob/master/notebooks/2_Chu_State_Task_Network.ipynb).
* [Example from Maravelias and Grossmann, 2003](http://nbviewer.jupyter.org/github/jckantor/STN-Scheduler/blob/master/notebooks/4_Maravelias_Grossmann_Example_A.ipynb).
* [Classroom Case Study of a Multipurpose Batch Fermentation Plant (to be finished)](http://nbviewer.jupyter.org/github/jckantor/STN-Scheduler/blob/master/notebooks/3_Multipurpose_Fermentation_Plant.ipynb).

This module implements the STN model using the Pyomo package for building optimization models in [Python](http://www.pyomo.org/), and requires an MILP solver to compute schedules.

![](images/Kondili_gantt.png)


## Dependencies

* [Pyomo](http://www.pyomo.org/)
* An MILP solver is required for computing solutions to the MILP scheduling problems. The module has been tested with GLPK and Gurobi.

## Related Projects

* [pySTN](https://github.com/robin-vjc/pySTN) Implementation of a robust scheduling system based on STN (State-Task-Network) models.
