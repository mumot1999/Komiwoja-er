import pytest

from exceptions import VisitedNodeError
from main import (
    Nodes
)


def my_map(function, list):
    new_list = []
    for el in list:
        new_list.append(function(el))
    return new_list

def my_filter(function, list):
    new_list = []
    for el in list:
        if (function(el)):
            new_list.append(el)

    return new_list



def test_second_connection_should_be_not_allowed():
    nodes = Nodes(2)
    nodes.connect(0, 1)
    nodes.connect(1, 0)

    assert 1 == len(nodes[0].neighbors)


def test_visit_when_no_connection_should_throw_exception():
    nodes = Nodes(2)
    with pytest.raises(VisitedNodeError) as e:
        nodes[0].visit_node(nodes[1])
        assert e.message == 'Node is not in neighbours'


def test_visit_visited_node_should_throw_exception():
    nodes = Nodes(2)
    nodes.connect(0, 1)
    nodes[1].visit_node(nodes[0])

    assert [] == nodes[1].neighbors
    assert [] == nodes[0].neighbors

    with pytest.raises(VisitedNodeError):
        nodes[0].visit_node(nodes[1])


def test_delete_neighbour():
    nodes = Nodes(2)
    nodes.connect(0, 1)
    nodes[0].neighbors[0].delete_neighbour(0)
    nodes[0].delete_neighbour(1)
    assert [] == nodes[0].neighbors
    assert [] == nodes[1].neighbors


def test_visit_node():
    nodes = Nodes(2)
    nodes.connect(0, 1)
    nodes[1].visit_node(nodes[0])
    assert True


def test_find_ways():
    nodes = Nodes(4)
    nodes.connect(0, 1)
    nodes.connect(1, 2)
    nodes.connect(1, 3)
    nodes.connect(2, 3)
    nodes.connect(3, 0)

    ways = nodes.find_ways(nodes[0])
    assert [0, 1, 2, 3, 0] in ways
    assert [0, 3, 2, 1, 0] in ways


def test_find_ways_1():
    nodes = Nodes(3)
    nodes.connect(0, 1)
    nodes.connect(1, 2)
    nodes.connect(2, 0)

    ways = nodes.find_ways(nodes[0])
    assert 2 == len(ways)
    assert [
               [0, 1, 2, 0],
               [0, 2, 1, 0],
           ] == ways


def test_find_ways_one_way():
    nodes = Nodes(3)
    nodes.connect(0, 1)
    nodes.connect(1, 2)

    ways = nodes.find_ways(nodes[0])
    assert [[0, 1, 2]] == ways


def test_map():
    items = [{'id': 1, 'v': 'asd'}, {'id': 2, 'v': 'as2'}]


    def transform_function(item):
        return item['id']

    lambda_transform = lambda x: x['id']

    assert [1, 2] == my_map(transform_function, items)
    assert [1, 2] == my_map(lambda_transform, items)


def test_run():
    nodes = Nodes(3)
    nodes.connect(0, 1)
    nodes.connect(1, 2)
    nodes.connect(2, 0)

    assert 6 == len(nodes.run())


def test_good_run():
    nodes = Nodes(4)
    nodes.connect(0, 1)
    nodes.connect(1, 2)
    nodes.connect(1, 3)
    nodes.connect(2, 3)
    nodes.connect(3, 0)

    ways = nodes.get_good_ways()
    print(ways)

    assert 8 == len(ways)

    ways = nodes.find_ways(nodes[1])
    print(ways)


def test_good_run_2():
    nodes = Nodes(5)
    nodes.connect(0, 4)
    nodes.connect(0, 1)
    nodes.connect(0, 2)
    nodes.connect(0, 3)

    nodes.connect(1, 2)

    nodes.connect(2, 3)

    assert 0 == len(nodes.get_good_ways())
