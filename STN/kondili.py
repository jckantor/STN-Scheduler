#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 08:37:40 2017

@author: jeff
"""

import sys
sys.path.append('../STN')
from STN import STN

# create instance
stn = STN()

# states
stn.state('FeedA',     init = 200)
stn.state('FeedB',     init = 200)
stn.state('FeedC',     init = 200)
stn.state('HotA',      price = -1)
stn.state('IntAB',     price = -1)
stn.state('IntBC',     price = -1)
stn.state('ImpureE',   price = -1)
stn.state('Product_1', price = 10)
stn.state('Product_2', price = 10)

# state to task arcs
stn.stArc('FeedA',   'Heating')
stn.stArc('FeedB',   'Reaction_1', rho = 0.5)
stn.stArc('FeedC',   'Reaction_1', rho = 0.5)
stn.stArc('FeedC',   'Reaction_3', rho = 0.2)
stn.stArc('HotA',    'Reaction_2', rho = 0.4)
stn.stArc('IntAB',   'Reaction_3', rho = 0.8)
stn.stArc('IntBC',   'Reaction_2', rho = 0.6)
stn.stArc('ImpureE', 'Separation')

# task to state arcs
stn.tsArc('Heating',    'HotA',      rho = 1.0, dur = 1)
stn.tsArc('Reaction_2', 'IntAB',     rho = 0.6, dur = 2)
stn.tsArc('Reaction_2', 'Product_1', rho = 0.4, dur = 2)
stn.tsArc('Reaction_1', 'IntBC',     dur = 2)
stn.tsArc('Reaction_3', 'ImpureE',   dur = 1)
stn.tsArc('Separation', 'IntAB',     rho = 0.1, dur = 2)
stn.tsArc('Separation', 'Product_2', rho = 0.9, dur = 1)

# unit-task data
stn.unit('Heater',    'Heating',    Bmin = 0, Bmax = 100)
stn.unit('Reactor_1', 'Reaction_1', Bmin = 0, Bmax =  80)
stn.unit('Reactor_1', 'Reaction_2', Bmin = 0, Bmax =  80)
stn.unit('Reactor_1', 'Reaction_3', Bmin = 0, Bmax =  80)
stn.unit('Reactor_2', 'Reaction_1', Bmin = 0, Bmax =  50)
stn.unit('Reactor_2', 'Reaction_2', Bmin = 0, Bmax =  50)
stn.unit('Reactor_2', 'Reaction_3', Bmin = 0, Bmax =  50)
stn.unit('Still',     'Separation', Bmin = 0, Bmax = 200)

H = 10
stn.build(range(0,H+1))
stn.solve('glpk')
stn.gantt()
stn.trace()