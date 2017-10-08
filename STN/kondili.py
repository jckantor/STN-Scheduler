#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 05:44:56 2017

@author: jeff
"""

import sys
sys.path.append('../STN')
from STN import STN

# create instance
stn = STN()

# states
stn.state("FeedA", init = 200)
stn.state("FeedB", init = 200)
stn.state("FeedC", init = 200)
stn.state("IntBC")
stn.state("Product_1", price = 10)
stn.state("Product_2", price = 10)

# state to task arcs
stn.STarc("FeedA", "Heating")
stn.STarc("FeedB", "Reaction_1", rho = 0.5)
stn.STarc("FeedC", "Reaction_1", rho = 0.5)
stn.STarc("FeedC", "Reaction_3", rho = 0.2)
stn.STarc("HotA", "Reaction_2", rho = 0.4)
stn.STarc("IntAB", "Reaction_3", rho = 0.8)
stn.STarc("IntBC", "Reaction_2", rho = 0.6)
stn.STarc("ImpureE", "Separation")

# task to state arcs
stn.TSarc("Heating", "HotA", 1, 1)
stn.TSarc("Reaction_2", "IntAB", rho=0.6, dur=2)
stn.TSarc("Reaction_2", "Product_1", rho=0.4, dur=2)
stn.TSarc("Reaction_1", "IntBC", dur=2)
stn.TSarc("Reaction_3", "ImpureE", dur=1)
stn.TSarc("Separation", "IntAB", rho=0.1, dur=2)
stn.TSarc("Separation", "Product_2", rho=0.9, dur=1)

# unit-task data
stn.Unit("Heater", "Heating", 0, 100)
stn.Unit("Reactor_1", "Reaction_1", 0, 80)
stn.Unit("Reactor_1", "Reaction_2", 0, 80)
stn.Unit("Reactor_1", "Reaction_3", 0, 80)
stn.Unit("Reactor_2", "Reaction_1", 0, 50)
stn.Unit("Reactor_2", "Reaction_2", 0, 50)
stn.Unit("Reactor_2", "Reaction_3", 0, 50)
stn.Unit("Still", "Separation", 0, 200)

stn.buildmodel()
stn.solve()
stn.gantt()