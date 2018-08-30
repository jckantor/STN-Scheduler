class State():

    def __init__(self, name, initial=0, capacity=float('inf'), price=0):
        self.name = name
        self.initial = initial
        self.capacity = capacity
        self.price = price

    def __repr__(self):
        return 'State("{0}", {1}, {2}, {3})'.format(
            self.name, self.initial, self.capacity, self.price)


class Task():

    def __init__(self, name):
        self.name = name
        self.feeds = dict()
        self.products = dict()

    def __repr__(self):
        return self.name


class Flow():

    def __init__(self, state, task, rho=1, dur=0):
        self.state = state
        self.task = task
        self.rho = rho
        self.dur = dur

    def __repr__(self):
        return 'Flow({0}, {1}, {2}, {3}'.format(
            self.state, self.task, self.rho, self.dur)


class Unit():

    def __init__(self, name, Bmin=0, Bmax=float('inf'), tclean=0, fcost=0, vcost=0):
        self.name = name
        self.tasks = []
        self.Bmin = Bmin
        self.Bmax = Bmax
        self.tclean = tclean
        self.fcost = fcost
        self.vcost = vcost

    def __repr__(self):
        return self.name


class STN:

    def __init__(self):
        self._states = set()
        self._tasks = set()
        self._inflows = set()
        self._outflows = set()
        self._units = set()

    def __setattr__(self, name, value):
        if type(value) == State:
            self._states.add(name)
        elif type(value) == Task:
            self._tasks.add(name)
        elif type(value) == Unit:
            self._units.add(name)
        self.__dict__[name] = value


#    def __repr__(self):
#        print(self.feeds)
#        print(self.products)
#        print(self.units)
#        return "<Task>" + self.name

"""
    def feed(self, name, rho=1, dur=0):
        self.feeds[name] = {'rho': rho, 'dur': dur}

    def product(self, name, rho=1, dur=0):
        self.products[name] = {'rho': rho, 'dur': dur}

    def unit(self, name, Bmin=0, Bmax=np.Inf, tclean=0, cost=0, vcost=0):
        self.units[name] = {
            'Bmin': Bmin,
            'Bmax': Bmax,
            'tclean': tclean,
            'cost': cost,
            'vcost': vcost}
        name.tasks[self] = {
            'Bmin': Bmin,
            'Bmax': Bmax,
            'tclean': tclean,
            'cost': cost,
            'vcost': vcost}
"""

"""
class Unit():

    def __init__(self, name):
        self.name = name
        self.tasks = dict()

    def __repr__(self):
        return "<Unit>" + self.name


    def task(self, name, Bmin=0, Bmax=np.Inf, tclean=0, cost=0, vcost=0):
        self.tasks[name] = {
            'Bmin': Bmin,
            'Bmax': Bmax,
            'tclean': tclean,
            'cost': cost,
            'vcost': vcost}
        name.units[self] = {
            'Bmin': Bmin,
            'Bmax': Bmax,
            'tclean': tclean,
            'cost': cost,
            'vcost': vcost}
"""




"""
    def __repr__(self):
        s = "States:\n"
        for name in sorted(self._states):
            state = getattr(self, name)
            s += "    {0:20s}".format(str(state))
            s += "    {0:6.1f}".format(state.price)
            s += "    {0:6.1f}".format(state.initialize)
            s += "    {0:6.1f}\n".format(state.capacity)

        s += "\nTasks:\n"
        for name in sorted(self._tasks):
            task = getattr(self, name)
            s += "    {0:12s}\n".format(str(task))
            print(task.feeds)
            for f in task.feeds:
                s += "           Feed: {0:12s}".format(str(f))
                print(s)
                print(getattr(f, 'name'))
                s += "  {0:4.2f}".format(getattr(self, f)['rho'])
                s += "\n"
            s += "\n"
            # for f in task.feeds:
            #    s += "\n           Feed: {0:12s}".format(str(f))
            #    s += "  {0:4.2f}".format(self.feeds[f]['rho'])
            #    s += "  {0:4.2f}".format(self.feeds[f]['dur'])

        s += "\nUnits:\n"
        for name in sorted(self._units):
            unit = getattr(self, name)
            s += "    {0:12s}\n".format(str(unit))
        return s

"""

# class Feed():
#    def __init__(state, task, rho=1, dur=0):


