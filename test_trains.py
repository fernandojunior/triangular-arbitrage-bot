from trains.trains import *  # noqa


def test_create_graph():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert g.nodes == {'C', 'D', 'E', 'B', 'A'}
    assert g.distances == {('A', 'D'): 5, ('E', 'B'): 3, ('D', 'C'): 8, ('D', 'E'): 6, ('C', 'E'): 2, ('A', 'E'): 7,
                           ('C', 'D'): 8, ('B', 'C'): 4, ('A', 'B'): 5}


def test_dijsktra():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert dijsktra(g, "A") == ({'E': 7, 'A': 0, 'C': 9, 'B': 5, 'D': 5}, {'E': 'A', 'C': 'B', 'B': 'A', 'D': 'A'})
    """
    ({'C': 4, 'B': 0, 'E': 6, 'D': 12}, {'C': 'B', 'E': 'C', 'D': 'C'})
    """


def test_route_verification():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert route_verification("A-B-C", g) == '9'
    assert route_verification("A-D", g) == '5'
    assert route_verification("A-D-C", g) == '13'
    assert route_verification("A-E-B-C-D", g) == '22'
    assert route_verification("A-E-D", g) == 'NO SUCH ROUTE'
    assert route_verification("C->C, S <= 3", g) == 2
    assert route_verification("A->C, S == 4", g) == 3
    # assert route_verification("A->C, L<", g) == 9
    # assert route_verification("B->B, L<", g) == 9
    # assert route_verification("C->C, L<30", g) == 7


def test_simple_route():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert route_distance("A-B-C", g) == '9'
    assert route_distance("A-D", g) == '5'
    assert route_distance("A-D-C", g) == '13'
    assert route_distance("A-E-B-C-D", g) == '22'
    assert route_distance("A-E-D", g) == 'NO SUCH ROUTE'


def test_complex_route():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert complex_route("C->C, S <= 3", g) == 2
    assert complex_route("A->C, S == 4", g) == 3
    #   assert complex_route("A->C, L<", g) == 9
    #   assert complex_route("B->B, L<", g) == 9
    #   assert complex_route("C->C, L<30", g) == 7


def test_mysplit():
    assert mysplit("/", "/") == []
    assert mysplit("/a", "/") == ['a']
    assert mysplit("/a/a", "/") == ['a', 'a']
    assert mysplit("/a/a/a/", "/") == ['a', 'a', 'a']


def test_count_routes():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    assert count_routes(g, start_node="C", max_stops=3, end_node="C") == 2
    assert count_routes(g, start_node="A", max_stops=4, end_node="C", operator="==") == 3
    # A to C (via B,C,D); A to C (via D,C,D); and A to C (via D,E,B)
    # A B C D C
    # A D C D C
    # A D E B C


def test_run_route_len():
    g = Graph("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7")
    # assert run_route_len( g, start_node = "A", end_node="C", operator="<") == 9
    # assert run_route_len( g, start_node = "B", end_node="B", operator="<") == 9
    # assert route_verification("C->C, L<30", g) == 7
    assert run_route_len3(g, start_node="C", end_node="C", max_dist=30) == 7

    """CDC"""
    """ CEBC"""
    """CEBCDC"""
    """CDCEBC"""
    # CDEBC
    """ CEBCEBC """
    """ CEBCEBCEBC """
