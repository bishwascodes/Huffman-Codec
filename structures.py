# Project 2
# Bishwas, Advanced Algorithm, 9/11/2026

import random
import pytest

# Graph ADT
class Graph:

    def __init__(self, nodes=(), edges=()):
    
        self._node_data = {}
        self._children = {}
        self._parents = {}
        self._edge_data = {}

        for item in nodes:
            if isinstance(item, tuple) and len(item) == 2:
                self.add_node(item[0], data=item[1])
            else:
                self.add_node(item)

        for edge in edges:
            parent, child, *rest = edge
            self.add_node(parent)
            self.add_node(child)
            self.add_edge(parent, child, data=rest[0] if rest else None)


    def add_node(self, node, data=None):
        if node not in self._node_data:
            self._node_data[node] = data
            self._children[node] = {}
            self._parents[node] = {}

    def add_edge(self, parent, child, data=None):
        if parent not in self._node_data:
            raise KeyError(f"node not in graph: {parent!r}")
        if child not in self._node_data:
            raise KeyError(f"node not in graph: {child!r}")
        # keep both directions so get_children and get_parents don't need a scan
        self._children[parent][child] = None
        self._parents[child][parent] = None
        self._edge_data[(parent, child)] = data

    def add_undirected_edge(self, node1, node2, data=None):
        self.add_edge(node1, node2, data=data)
        self.add_edge(node2, node1, data=data)


    def get_node_data(self, node):
        return self._node_data[node]

    def get_edge_data(self, parent, child):
        return self._edge_data[(parent, child)]

    def get_children(self, parent):
        return self._children[parent].keys()

    def get_parents(self, node):
        return self._parents[node].keys()

    def contains_node(self, node):
        return node in self._node_data

    def contains_edge(self, parent, child):
        return (parent, child) in self._edge_data

    def get_nodes(self):
        return self._node_data.keys()

    def get_edges(self):
        return self._edge_data.keys()

# Priority Queue
class _Entry:

    __slots__ = ("key", "priority", "data")

    def __init__(self, key, priority, data):
        self.key = key
        self.priority = priority
        self.data = data

    def __repr__(self):
        return f"_Entry({self.key!r}, {self.priority!r}, {self.data!r})"


class PriorityQueue:

    def __init__(self, items=()):
        self._heap = []
        self._positions = {}  # key -> its index in _heap, so we don't have to search for it
        for item in items:
            key, priority, *rest = item
            self.update(key, priority, data=rest[0] if rest else None)

    # internal functions 
    def _swap(self, i, j):
        heap = self._heap
        heap[i], heap[j] = heap[j], heap[i]
        # positions has to move with them or lookups start pointing at the wrong entry
        self._positions[heap[i].key] = i
        self._positions[heap[j].key] = j

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i].priority < self._heap[parent].priority:
                self._swap(i, parent)
                i = parent
            else:
                break
        return i

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            left = 2 * i + 1
            right = left + 1
            smallest = i
            if left < n and self._heap[left].priority < self._heap[smallest].priority:
                smallest = left
            if right < n and self._heap[right].priority < self._heap[smallest].priority:
                smallest = right
            if smallest == i:
                return i
            self._swap(i, smallest)
            i = smallest


    def update(self, key, priority, data=None, only_if_less=False):
        index = self._positions.get(key)

        if index is None:
            entry = _Entry(key, priority, data)
            self._heap.append(entry)
            index = len(self._heap) - 1
            self._positions[key] = index
            self._sift_up(index)
            return

        entry = self._heap[index]
        if only_if_less and not (priority < entry.priority):
            return  # caller only wants it if it's an improvement and it isn't

        old_priority = entry.priority
        entry.priority = priority
        entry.data = data
        # priority only moved in one direction so, only one of these can do anything
        if priority < old_priority:
            self._sift_up(index)
        elif old_priority < priority:
            self._sift_down(index)

    def peek_min(self):
        if not self._heap:
            raise IndexError("peek_min from an empty priority queue")
        return self._heap[0].key

    def remove(self, key):
        index = self._positions.pop(key)
        last = self._heap.pop()
        if index < len(self._heap):
            # last moved into the hole
            self._heap[index] = last
            self._positions[last.key] = index
            self._sift_up(index)
            self._sift_down(index)

    def contains_key(self, key):
        return key in self._positions

    def get_data(self, key):
        return self._heap[self._positions[key]].data

    def get_priority(self, key):
        return self._heap[self._positions[key]].priority

    def count(self):
        return len(self._heap)



# Prim's Minimum Spanning Tree

def prim_mst(graph, edge_weight=None, start_node=None):
    """
    Find minimum spanning tree using Prim's algorithm.
    
    Args:
        graph: an instance of your Graph data structure
        start_node: the node to start from; if None, uses first node from graph.get_nodes()
        edge_weight: function taking (parent, child) returning edge weight;
                     if None, uses edge data as weight
    
    Returns:
        Graph instance containing the minimum spanning tree
    """
    if edge_weight is None:
        edge_weight = lambda parent, child: graph.get_edge_data(parent, child)
    
    if start_node is None:
        start_node = next(iter(graph.get_nodes()))
    
    mst = Graph()  # assuming your Graph class is named Graph
    pq = PriorityQueue()  # assuming your PriorityQueue class is named PriorityQueue
    
    pq.update(start_node, 0, data=None)
    
    while pq.count() > 0:
        current_node = pq.peek_min()
        parent_node = pq.get_data(current_node)
        pq.remove(current_node)
        
        if not mst.contains_node(current_node):
            mst.add_node(current_node)
            if parent_node is not None:
                data = graph.get_edge_data(parent_node, current_node)
                mst.add_undirected_edge(parent_node, current_node, data=data)
            
            for child in graph.get_children(current_node):
                if not mst.contains_node(child):
                    weight = edge_weight(current_node, child)
                    pq.update(child, weight, data=current_node, only_if_less=True)
    
    return mst


# Graph ADT Tests

def test_new_graph_has_no_nodes():
    graph = Graph()
    assert list(graph.get_nodes()) == []


def test_add_node_then_contains_node():
    graph = Graph()
    graph.add_node("a")
    assert graph.contains_node("a")
    assert not graph.contains_node("b")


def test_add_node_is_idempotent():
    graph = Graph()
    graph.add_node("a", data=1)
    graph.add_node("a", data=2)  # already present 
    assert list(graph.get_nodes()) == ["a"]


def test_get_node_data():
    graph = Graph()
    graph.add_node("a", data="hello")
    assert graph.get_node_data("a") == "hello"


def test_add_edge_then_contains_edge():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", data=5)
    assert graph.contains_edge("a", "b")
    assert not graph.contains_edge("b", "a")  # directed so the reverse shouldn't exist


def test_get_edge_data():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", data=5)
    assert graph.get_edge_data("a", "b") == 5


def test_add_undirected_edge_creates_both_directions():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_undirected_edge("a", "b", data=7)
    assert graph.contains_edge("a", "b")
    assert graph.contains_edge("b", "a")
    assert graph.get_edge_data("a", "b") == 7
    assert graph.get_edge_data("b", "a") == 7


def test_get_children():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_node("c")
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    assert set(graph.get_children("a")) == {"b", "c"}


def test_get_nodes_preserves_insertion_order():
    graph = Graph()
    graph.add_node("c")
    graph.add_node("a")
    graph.add_node("b")
    assert list(graph.get_nodes()) == ["c", "a", "b"]


def test_get_edges_preserves_insertion_order():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_node("c")
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    assert list(graph.get_edges()) == [("a", "b"), ("a", "c")]


def test_contains_node_false_for_absent_node():
    graph = Graph()
    assert not graph.contains_node("nonexistent")


def test_contains_edge_false_for_absent_edge():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    assert not graph.contains_edge("a", "b")


# more tests for get_parents

def test_get_parents():
    graph = Graph()
    for node in ("a", "b", "c"):
        graph.add_node(node)
    graph.add_edge("a", "c")
    graph.add_edge("b", "c")
    assert set(graph.get_parents("c")) == {"a", "b"}


def test_get_parents_is_empty_for_source_node():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b")
    assert list(graph.get_parents("a")) == []


def test_get_parents_respects_edge_direction():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b")
    assert list(graph.get_parents("b")) == ["a"]
    assert list(graph.get_children("b")) == []


def test_get_parents_sees_both_ends_of_an_undirected_edge():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_undirected_edge("a", "b")
    assert list(graph.get_parents("a")) == ["b"]
    assert list(graph.get_parents("b")) == ["a"]


def test_get_parents_does_not_duplicate_a_repeated_edge():
    graph = Graph()
    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b", data=1)
    graph.add_edge("a", "b", data=2)  # same edge, new data
    assert list(graph.get_parents("b")) == ["a"]
    assert graph.get_edge_data("a", "b") == 2


# Priority Queue Tests

def test_new_priority_queue_has_count_zero():
    pq = PriorityQueue()
    assert pq.count() == 0


def test_update_adds_new_key():
    pq = PriorityQueue()
    pq.update("a", 5)
    assert pq.count() == 1
    assert pq.contains_key("a")


def test_peek_min_returns_smallest_priority_key():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 2)
    pq.update("c", 9)
    assert pq.peek_min() == "b"


def test_peek_min_does_not_remove():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.peek_min()
    assert pq.count() == 1
    assert pq.contains_key("a")


def test_get_data_returns_associated_data():
    pq = PriorityQueue()
    pq.update("a", 5, data="hello")
    assert pq.get_data("a") == "hello"


def test_update_existing_key_changes_priority_without_duplicating():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 1)
    pq.update("a", 0)  # a should now be the minimum
    assert pq.peek_min() == "a"
    assert pq.count() == 2  # still just two keys, not duplicated


def test_update_only_if_less_ignores_higher_priority():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("a", 10, only_if_less=True)  # 10 is not less than 5 -- should be ignored
    pq.update("b", 7)
    assert pq.peek_min() == "a"  # a's priority should still be 5, which beats 7


def test_update_only_if_less_applies_lower_priority():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 3)
    pq.update("a", 1, only_if_less=True)  # 1 is less than 5 
    assert pq.peek_min() == "a"


def test_update_only_if_less_on_new_key_still_adds_it():
    pq = PriorityQueue()
    pq.update("a", 5, only_if_less=True)  # a wasn't present yet 
    assert pq.contains_key("a")
    assert pq.count() == 1


def test_remove_deletes_key():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 2)
    pq.remove("b")
    assert not pq.contains_key("b")
    assert pq.count() == 1
    assert pq.peek_min() == "a"


def test_remove_then_reinsert():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.remove("a")
    pq.update("a", 1)
    assert pq.contains_key("a")
    assert pq.peek_min() == "a"


def test_contains_key_false_for_absent_key():
    pq = PriorityQueue()
    assert not pq.contains_key("nonexistent")


def test_many_updates_and_removes_maintain_min_heap_order():
    pq = PriorityQueue()
    for key, priority in [("a", 5), ("b", 2), ("c", 8), ("d", 1), ("e", 9), ("f", 3)]:
        pq.update(key, priority)
    order = []
    while pq.count() > 0:
        m = pq.peek_min()
        order.append(m)
        pq.remove(m)
    assert order == ["d", "b", "f", "a", "c", "e"]


# more tests for get_priority

def test_get_priority():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("b", 2)
    assert pq.get_priority("a") == 5
    assert pq.get_priority("b") == 2


def test_get_priority_reflects_an_update():
    pq = PriorityQueue()
    pq.update("a", 5)
    pq.update("a", 1)
    assert pq.get_priority("a") == 1


def test_get_priority_unchanged_when_only_if_less_blocks_the_update():
    pq = PriorityQueue()
    pq.update("a", 5, data="original")
    pq.update("a", 10, data="ignored", only_if_less=True)
    assert pq.get_priority("a") == 5
    assert pq.get_data("a") == "original"  # a blocked update changes nothing


def test_get_priority_raises_for_absent_key():
    pq = PriorityQueue()
    with pytest.raises(KeyError):
        pq.get_priority("nonexistent")


def test_get_priority_after_a_raised_priority_sifts_down():
    pq = PriorityQueue()
    for key, priority in [("a", 1), ("b", 2), ("c", 3), ("d", 4)]:
        pq.update(key, priority)
    pq.update("a", 99)
    assert pq.get_priority("a") == 99
    assert pq.peek_min() == "b"
    assert [pq.get_priority(k) for k in ("b", "c", "d")] == [2, 3, 4]




# Prim's MST tests

def build_undirected_graph(weighted_edges):
    graph = Graph()
    for node1, node2, _weight in weighted_edges:
        graph.add_node(node1)
        graph.add_node(node2)
    for node1, node2, weight in weighted_edges:
        graph.add_undirected_edge(node1, node2, data=weight)
    return graph


def mst_edge_set(mst):
    return {frozenset(edge) for edge in mst.get_edges()}


def mst_total_weight(mst):
    total = sum(mst.get_edge_data(parent, child) for parent, child in mst.get_edges())
    return total / 2



# small graph with distinct weights
SMALL_EDGES = [("a", "b", 1), ("b", "c", 2), ("a", "c", 5), ("c", "d", 3), ("b", "d", 6)]


def test_prim_on_single_node_graph():
    graph = Graph()
    graph.add_node("a")
    mst = prim_mst(graph)
    assert list(mst.get_nodes()) == ["a"]
    assert list(mst.get_edges()) == []


def test_prim_on_two_node_graph():
    graph = build_undirected_graph([("a", "b", 4)])
    mst = prim_mst(graph)
    assert set(mst.get_nodes()) == {"a", "b"}
    assert mst_edge_set(mst) == {frozenset({"a", "b"})}
    assert mst.get_edge_data("a", "b") == 4


def test_prim_finds_the_unique_minimum_spanning_tree():
    mst = prim_mst(build_undirected_graph(SMALL_EDGES))
    assert set(mst.get_nodes()) == {"a", "b", "c", "d"}
    assert mst_edge_set(mst) == {
        frozenset({"a", "b"}),
        frozenset({"b", "c"}),
        frozenset({"c", "d"}),
    }
    assert mst_total_weight(mst) == 6


def test_prim_result_is_a_tree():
    mst = prim_mst(build_undirected_graph(SMALL_EDGES))
    node_count = len(list(mst.get_nodes()))
    # Undirected edges are stored twice, so a spanning tree has 2(n-1) of them.
    assert len(list(mst.get_edges())) == 2 * (node_count - 1)


def test_prim_mst_edges_carry_the_original_weights():
    mst = prim_mst(build_undirected_graph(SMALL_EDGES))
    graph = build_undirected_graph(SMALL_EDGES)
    for parent, child in mst.get_edges():
        assert mst.get_edge_data(parent, child) == graph.get_edge_data(parent, child)


def test_prim_gives_the_same_tree_from_any_start_node():
    graph = build_undirected_graph(SMALL_EDGES)
    trees = [mst_edge_set(prim_mst(graph, start_node=node)) for node in "abcd"]
    assert all(tree == trees[0] for tree in trees)


def test_prim_rejects_a_tempting_but_suboptimal_first_edge():
    graph = build_undirected_graph([("a", "b", 1), ("a", "c", 2), ("b", "c", 10)])
    mst = prim_mst(graph, start_node="a")
    assert mst_edge_set(mst) == {frozenset({"a", "b"}), frozenset({"a", "c"})}
    assert mst_total_weight(mst) == 3


def test_prim_lowers_a_priority_already_in_the_queue():
    graph = build_undirected_graph(
        [("a", "b", 1), ("a", "c", 2), ("a", "d", 9), ("c", "d", 1)]
    )
    mst = prim_mst(graph, start_node="a")
    assert mst_edge_set(mst) == {
        frozenset({"a", "b"}),
        frozenset({"a", "c"}),
        frozenset({"c", "d"}),
    }
    assert mst_total_weight(mst) == 4


def test_prim_with_a_custom_edge_weight_function():
    graph = Graph()
    for node in "abcd":
        graph.add_node(node)
    for node1, node2, weight in SMALL_EDGES:
        graph.add_undirected_edge(node1, node2, data={"weight": weight, "label": "road"})

    mst = prim_mst(graph, edge_weight=lambda p, c: graph.get_edge_data(p, c)["weight"])
    assert mst_edge_set(mst) == {
        frozenset({"a", "b"}),
        frozenset({"b", "c"}),
        frozenset({"c", "d"}),
    }


def test_prim_handles_ties_and_still_returns_a_spanning_tree():
    graph = build_undirected_graph(
        [("a", "b", 1), ("b", "c", 1), ("c", "d", 1), ("d", "a", 1)]
    )
    mst = prim_mst(graph)
    assert set(mst.get_nodes()) == {"a", "b", "c", "d"}
    assert mst_total_weight(mst) == 3


def test_prim_spans_only_the_component_of_the_start_node():
    graph = build_undirected_graph([("a", "b", 1), ("c", "d", 1)])
    mst = prim_mst(graph, start_node="a")
    assert set(mst.get_nodes()) == {"a", "b"}


def test_prim_on_the_classic_clrs_graph():
    edges = [
        ("a", "b", 4), ("a", "h", 8), ("b", "h", 11), ("b", "c", 8),
        ("h", "i", 7), ("h", "g", 1), ("i", "c", 2), ("i", "g", 6),
        ("g", "f", 2), ("c", "f", 4), ("c", "d", 7), ("d", "f", 14),
        ("d", "e", 9), ("f", "e", 10),
    ]
    mst = prim_mst(build_undirected_graph(edges))
    assert set(mst.get_nodes()) == set("abcdefghi")
    assert mst_total_weight(mst) == 37
    assert len(list(mst.get_edges())) == 2 * (9 - 1)



