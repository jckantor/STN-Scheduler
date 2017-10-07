#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 17:42:12 2017

@author: jeff
"""

from pyomo.environ import *
from pprint import pprint
import numpy as np

class STN(object):
    
    def __init__(self):
        # simulation objects
        self.states = set()         # set of state names
        self.tasks = set()          # set of task names
        self.units = set()          # set of unit names

        # dictionaries indexed by task name
        self.S = {}                 # sets of states feeding each task (inputs)
        self.S_ = {}                # sets of states fed by each task (outputs)
        self.K = {}                 # sets of units capable of each task 
        self.p = {}                 # task durations
        
        # dictionaries indexed by state name
        self.T = {}                 # sets of tasks fed from each state (task output)
        self.T_ = {}                # sets of tasks feeding each state (task inputs)
        self.C = {}                 # capacity of each task
        self.init = {}              # initial level
        self.price = {}             # prices of each state
        
        # dictionaries indexed by (task,state) tuples
        self.rho = {}               # input feed fractions indexed by (task,state)
        self.rho_ = {}              # output product dispositions by (task,state)
        self.P = {}                 # time to finish output from task to state (task, state)

        # dictionary indexed by unit
        self.I = {}                 # sets of tasks performed by each unit
        
        # characterization of units indexed by (task,unit)
        self.Vmax = {}              # max capacity of unit j performing tank i
        self.Vmin = {}              # minimum capacity of unit j performing task i
    
    # defines states as .state(name, capacity, init)
    def state(self, name, capacity=float('inf'), init=0, price=0,):
        self.states.add(name)       # add to the set of states
        self.C[name] = capacity     # state capacity
        self.init[name] = init      # state initial value
        self.T[name] = set()        # set of tasks which feed this state (inputs)
        self.T_[name] = set()       # set of tasks fed from this state (outputs)
        self.price[name] = price    # per unit price of each state
        
    def task(self, name):
        self.tasks.add(name)        # add to set of tasks
        self.S[name] = []           # set of states which feed this task (inputs)
        self.S_[name] = []          # set of states fed by this task (outputs)
        self.p[name] = 0            # completion time for this task
        self.K[name] = []
        
    def unit(self, name):
        self.units.add(name)
        self.I[name] = []
        
    def STarc(self,state,task,rho=1):
        if state not in self.states:
            self.state(state)
        if task not in self.tasks:
            self.task(task)
        self.S[task].append(state)  
        self.rho[(task,state)] = rho
        self.T[state].add(task)
        
    def TSarc(self,task,state,rho=1,dur=1):
        if state not in self.states:
            self.state(state)
        if task not in self.tasks:
            self.task(task)
        self.S_[task].append(state)
        self.T_[state].add(task)
        self.rho_[(task,state)] = rho
        self.P[(task,state)] = dur
        self.p[task] = max(self.p[task],dur)
        
    def Unit(self,unit,task,Vmin,Vmax):
        if unit not in self.units:
            self.unit(unit)
        if task not in self.tasks:
            self.task(task)
        self.I[unit].append(task)
        self.K[task].append(unit)
        self.Vmin[(task,unit)] = Vmin
        self.Vmax[(task,unit)] = Vmax
        
    def pprint(self):
        for task in sorted(self.tasks):
            print('\nTask:', task)
            print('    S[{0:s}]:'.format(task), self.S[task])
            print('    S_[{0:s}]:'.format(task), self.S_[task])
            print('    K[{0:s}]:'.format(task), self.K[task])
            print('    p[{0:s}]:'.format(task), self.p[task])

        for state in sorted(self.states):
            print('\nState:', state)
            print('    T[{0:s}]:'.format(state), self.T[state])
            print('    T_[{0:s}]:'.format(state), self.T_[state])
            print('    C[{0:s}]:'.format(state), self.C[state])
            print('    init[{0:s}]:'.format(state), self.init[state])
            
        for unit in sorted(self.units):
            print('\nUnit:', unit)
            print('    I[{0:s}]:'.format(unit), self.I[unit])
            
        print('\nState -> Task Arcs')  
        for (task,state) in sorted(self.rho.keys()):
            print('    {0:s} -> {1:s}:'.format(state,task))
            print('        rho:', self.rho[(task,state)])

        print('\nTask -> State Arcs')  
        for (task,state) in sorted(self.rho_.keys()):
            print('    {0:s} -> {1:s}:'.format(task,state))
            print('        rho_:', self.rho_[(task,state)])
            print('           P:', self.P[(task,state)])
            
    def buildmodel(self,tgrid = range(0,11)):
        
        self.tgrid = np.array([t for t in tgrid])
        self.H = max(self.tgrid)
        self.model = ConcreteModel()
        model = self.model
        model.cons = ConstraintList()
        
        # W[i,j,t] 1 if task i starts in unit j at time t
        model.W = Var(self.tasks, self.units, self.tgrid, domain=Boolean)
        
        # B[i,j,t] size of batch assigned to task i in unit j at time t
        model.B = Var(self.tasks, self.units, self.tgrid, domain=NonNegativeReals)
        
        # S[s,t] inventory of state s at time t
        model.S = Var(self.states, self.tgrid, domain=NonNegativeReals)
        
        # Q[j,t] inventory of unit j at time t
        model.Q = Var(self.units, self.tgrid, domain=NonNegativeReals)

        
        model.Value = Var(domain=NonNegativeReals)
        model.cons.add(self.model.Value == 
                       sum([self.price[s]*model.S[s,self.H] for s in self.states]))
        model.Obj = Objective(expr = model.Value, sense = maximize)
        
        # unit constraints
        for j in self.units:
            rhs = 0
            for t in self.tgrid:
                # a unit can only be allocated to one task 
                lhs = 0
                for i in self.I[j]:
                    for tprime in self.tgrid[(self.tgrid <= t) & (self.tgrid >= t-self.p[i]+1)]:
                        lhs += model.W[i,j,tprime]
                model.cons.add(lhs <= 1)
                
                # capacity constraints (see Konkili, Sec. 3.1.2)
                for i in self.I[j]:
                    model.cons.add(model.W[i,j,t]*self.Vmin[i,j] <= model.B[i,j,t])
                    model.cons.add(model.B[i,j,t] <= model.W[i,j,t]*self.Vmax[i,j])
                    
                # unit mass balance
                rhs += sum([model.B[i,j,t] for i in self.I[j]])
                for i in self.I[j]:
                    for s in self.S_[i]:
                        if t >= self.P[(i,s)]:
                            rhs -= self.rho_[(i,s)]*model.B[i,j,max(self.tgrid[self.tgrid <= t-self.P[(i,s)]])]
                model.cons.add(model.Q[j,t] == rhs)
                rhs = model.Q[j,t]
                
                # terminal condition  
                model.cons.add(model.Q[j,self.H] == 0)

        # state constraints
        for s in self.states:
            rhs = self.init[s]
            for t in self.tgrid:
                # state capacity constraint
                model.cons.add(model.S[s,t] <= self.C[s])
                # state mass balanace
                for i in self.T_[s]:
                    for j in self.K[i]:
                        if t >= self.P[(i,s)]: 
                            rhs += self.rho_[(i,s)]*model.B[i,j,max(self.tgrid[self.tgrid <= t-self.P[(i,s)]])]             
                for i in self.T[s]:
                    rhs -= self.rho[(i,s)]*sum([model.B[i,j,t] for j in self.K[i]])
                model.cons.add(model.S[s,t] == rhs)
                rhs = model.S[s,t] 

    def solve(self):
        self.solver = SolverFactory('glpk')
        self.solver.solve(self.model).write()

    def gantt(self):
        model = self.model
        C = self.C
        H = self.H
        I = self.I
        p = self.p
        plt.figure(figsize=(12,6))

        gap = H/400
        idx = 1
        lbls = []
        ticks = []
        for j in sorted(self.units):
            idx -= 1
            for i in sorted(I[j]):
                idx -= 1
                ticks.append(idx)
                lbls.append("{0:s} -> {1:s}".format(j,i))
                plt.plot([0,H],[idx,idx],lw=20,alpha=.3,color='y')
                for t in self.tgrid:
                    if model.W[i,j,t]() > 0:
                        plt.plot([t,t+p[i]], [idx,idx],'r', lw=20, alpha=0.5, solid_capstyle='butt')
                        plt.plot([t+gap,t+p[i]-gap], [idx,idx],'b', lw=16, solid_capstyle='butt')
                        txt = "{0:.2f}".format(model.B[i,j,t]())
                        plt.text(t+p[i]/2, idx, txt, color='white', weight='bold', ha='center', va='center')
        plt.xlim(0,self.H)
        plt.gca().set_yticks(ticks)
        plt.gca().set_yticklabels(lbls);
        