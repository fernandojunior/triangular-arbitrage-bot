from trains.trains import *  # noqa


def test_create_graph():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert g.nodes == {'C', 'D', 'E', 'B', 'A'}
    assert g.distances == {('A', 'D'): 5, ('E', 'B'): 3, ('D', 'C'): 8, ('D', 'E'): 6, ('C', 'E'): 2, ('A', 'E'): 7,
                           ('C', 'D'): 8, ('B', 'C'): 4, ('A', 'B'): 5}


def test_route_verification():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert route_distance(g, "A-B-C") == '9'
    assert route_distance(g, "A-D") == '5'
    assert route_distance(g, "A-D-C") == '13'
    assert route_distance(g, "A-E-B-C-D") == '22'
    assert route_distance(g, "A-E-D") == 'NO SUCH ROUTE'
    assert count_routes_by_stops(g, 'C', 'C', 3, operator="<=") == 2
    assert count_routes_by_stops(g, 'A', 'C', 4, operator="==") == 3
    assert shortest_route(g, 'A', 'C') == 9
    assert shortest_route(g, 'B', 'B') == 9
    assert count_routes_by_max_distance(g, 'C', 'C', max_distance=30) == 7
    # assert route_verification("A->C, L<", g) == 9
    # assert route_verification("B->B, L<", g) == 9
    # assert route_verification("C->C, L<30", g) == 7


def test_simple_route():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert route_distance(g, "A-B-C") == '9'
    assert route_distance(g, "A-D") == '5'
    assert route_distance(g, "A-D-C") == '13'
    assert route_distance(g, "A-E-B-C-D") == '22'
    assert route_distance(g, "A-E-D") == 'NO SUCH ROUTE'


def test_mysplit():
    assert mysplit("/", "/") == []
    assert mysplit("/a", "/") == ['a']
    assert mysplit("/a/a", "/") == ['a', 'a']
    assert mysplit("/a/a/a/", "/") == ['a', 'a', 'a']


def test_count_routes():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert count_routes_by_stops(g, start_node="C", stops=3, end_node="C") == 2
    assert count_routes_by_stops(g, start_node="A", stops=4, end_node="C", operator="==") == 3
    # A to C (via B,C,D); A to C (via D,C,D); and A to C (via D,E,B)
    # A B C D C
    # A D C D C
    # A D E B C
