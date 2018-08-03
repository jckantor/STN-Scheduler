import pytest
import numpy as np

from stn import State, Task, Unit, STN

def test_state_constructor():
    with pytest.raises(Exception):
        a = State()
    s = State('S')
    assert(hasattr(s, 'name'))
    assert(s.name == 'S')

    assert(hasattr(s, 'initial'))
    assert(s.initial == 0)

    assert(hasattr(s, 'price'))
    assert(s.price == 0)

    assert(hasattr(s, 'capacity'))
    assert(s.capacity == np.Inf)


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

    assert(hasattr(t, 'units'))
    assert(t.units == dict())


def test_unit_constructor():
    with pytest.raises(Exception):
        u = Unit()
    u = Unit('U')
    assert(hasattr(u, 'name'))
    assert(u.name == 'U')

    assert(hasattr(u, 'tasks'))
    assert(u.tasks == dict())


def test_stn_constructor():
    s = STN()
    assert(hasattr(s, '_states'))
    assert(hasattr(s, '_tasks'))
    assert(hasattr(s, '_units'))



