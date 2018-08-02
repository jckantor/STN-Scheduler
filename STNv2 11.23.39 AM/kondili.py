from STN import *


stn = STN(10)

# specify states
stn.feedA = State('FeedA', initialize=200)
stn.feedB = State('FeedB', initialize=200)
stn.feedC = State('FeedC', initialize=200)
stn.hotA  = State('HotA', capacity=100, price=-1)
stn.intAB = State('IntAB', capacity=200, price=-1)
stn.intBC = State('IntBC', capacity=150, price=-1)
stn.impureE = State('ImpureE', capacity=100, price=-1)
stn.product1 = State('Product_1', price=10)
stn.product2 = State('Product_2', price=10)

# specify tasks
stn.heating = Task('Heating')
stn.heating.feed(stn.feedA)

stn.reaction1 = Task('Reaction 1')
stn.reaction1.feed(stn.feedB, rho=0.5)
stn.reaction1.feed(stn.feedC, rho=0.5)
stn.reaction1.product(stn.product1, rho=0.4, dur=2)
stn.reaction1.product(stn.intAB, rho=0.6, dur=2)

stn.reaction2 = Task('Reaction 2')
stn.reaction2.feed(stn.hotA, rho=0.4)
stn.reaction2.feed(stn.intBC, rho=0.6)

stn.reaction3 = Task('Reaction 3')
stn.reaction3.feed(stn.feedC, rho=0.2)
stn.reaction3.feed(stn.intAB, rho=0.8)
stn.reaction3.product(stn.impureE, dur=1)

stn.separation = Task('Separation')
stn.separation.feed(stn.impureE)
stn.separation.product(stn.product2, rho=0.9, dur=1)
stn.separation.product(stn.intAB, rho=0.1, dur=2)

# specify units
stn.heater = Unit('Heater')
stn.heater.task(stn.heating, Bmax=200)

stn.reactor1 = Unit('Reactor_1')
stn.reactor1.task(stn.reaction1, Bmax=80)
stn.reactor1.task(stn.reaction2, Bmax=80)
stn.reactor1.task(stn.reaction3, Bmax=80)

stn.reactor2 = Unit('Reactor_2')
stn.reactor2.task(stn.reaction1, Bmax=50)
stn.reactor2.task(stn.reaction2, Bmax=50)
stn.reactor2.task(stn.reaction3, Bmax=50)

stn.still = Unit('Still')
stn.still.task(stn.separation, Bmax=200)
