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
stn.STarc('FeedA',   'Heating')
stn.STarc('FeedB',   'Reaction_1', rho = 0.5)
stn.STarc('FeedC',   'Reaction_1', rho = 0.5)
stn.STarc('FeedC',   'Reaction_3', rho = 0.2)
stn.STarc('HotA',    'Reaction_2', rho = 0.4)
stn.STarc('IntAB',   'Reaction_3', rho = 0.8)
stn.STarc('IntBC',   'Reaction_2', rho = 0.6)
stn.STarc('ImpureE', 'Separation')

# task to state arcs
stn.TSarc('Heating',    'HotA',      rho = 1.0, dur = 1)
stn.TSarc('Reaction_2', 'IntAB',     rho = 0.6, dur = 2)
stn.TSarc('Reaction_2', 'Product_1', rho = 0.4, dur = 2)
stn.TSarc('Reaction_1', 'IntBC',     dur = 2)
stn.TSarc('Reaction_3', 'ImpureE',   dur = 1)
stn.TSarc('Separation', 'IntAB',     rho = 0.1, dur = 2)
stn.TSarc('Separation', 'Product_2', rho = 0.9, dur = 1)

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
stn.buildmodel(range(0,H+1))
stn.solve('glpk')
stn.gantt()