import pytest

from stn import State, Task, Flow, Unit, STN

def test_state_constructor():
    with pytest.raises(Exception):
        a = State()
    s = State('S')
    assert(hasattr(s, 'name'))
    assert(s.name == 'S')

    assert(hasattr(s, 'initial'))
    assert(s.initial == 0)

    assert(hasattr(s, 'capacity'))
    assert(s.capacity == float('inf'))

    assert(hasattr(s, 'price'))
    assert(s.price == 0)

def test_task_constructor():
    with pytest.raises(Exception):
        t = Task()
    t = Task('T')
    assert(hasattr(t, 'name'))
    assert(t.name == 'T')

    assert(hasattr(t, 'feeds'))
    assert(t.feeds == dict())

    assert(hasattr(t, 'products'))
    assert(t.products == dict())

s = State('S')
t = Task('T')

def test_flow_constructor():
    with pytest.raises(Exception):
        f = Flow()
        f = Flow('F')
    f = Flow('F', s, t)
    assert(hasattr(f, 'state'))
    assert(hasattr(f, 'task'))
    assert(hasattr(f, 'rho'))
    assert(hasattr(f, 'dur'))


def test_unit_constructor():
    with pytest.raises(Exception):
        u = Unit()
    u = Unit('U')
    assert(hasattr(u, 'name'))
    assert(u.name == 'U')


def test_stn_constructor():
    s = STN()
    assert(hasattr(s, '_states'))
    assert(hasattr(s, '_tasks'))
    assert(hasattr(s, '_units'))



