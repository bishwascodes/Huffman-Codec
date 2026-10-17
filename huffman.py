#Bishwas - Fall 2026 - 10/16/26 - Adv Algo

#Greedy Huffman codec using the PriorityQueue from Project 2


from structures import PriorityQueue #old file from proj2


class Node: #each node has optional symbol, frequency, left, right and parent which are none by default
    def __init__(self, frequency, symbol=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = None
        self.right = None
        self.parent = None

    def is_leaf(self): #is leaf node if there are no any left or right nodes to it :)
        return self.left is None and self.right is None


class Codec:
    def __init__(self, root, leaves): #we need to now leaves and roots so that we know where to start for encoding and decoding
        self.root = root
        self.leaves = leaves

    def encode(self, symbols):
        for symbol in symbols:
            node = self.leaves[symbol]  #select the current symbol
            bits = [] #we don't know the symbol yet

            # we read upward from the leaf toward the root
            while node.parent is not None:
                parent = node.parent
                bits.append(0 if parent.left is node else 1)
                node = parent

            # If only one symbol - it won't have a parent but we can still give it 0 as its bit
            if not bits:
                bits.append(0)

            # reverse because we need from root to leaf - also using yield because provided test returns list based on ur yield generator 
            yield from reversed(bits)

    def decode(self, bits):
        root = self.root
        node = root

        for bit in bits:
            if bit not in (0, 1):
                raise ValueError("Invalid bits value")
            if root is None:
                raise ValueError("No root in the codec")

            # If only one symbol - it won't have a parent and the code is 0.
            if root.is_leaf():
                if bit != 0:
                    raise ValueError("Single node only tree must decode to 0")
                yield root.symbol
                continue

            node = node.left if bit == 0 else node.right
            if node is None:
                raise ValueError("Invalid bit sequence")

            if node.is_leaf():
                yield node.symbol
                node = root

        if root is not None and node is not root:
            raise ValueError("Incomplete bit sequence")


def huffman_codec(frequencies):
    pq = PriorityQueue()
    leaves = {}
    next_key = 0  # Unique heap keys, even for identical frequencies.

    for symbol, frequency in frequencies:
        if symbol in leaves:
            raise ValueError(f"Duplicate symbol: {symbol!r}")
        if frequency <= 0:
            raise ValueError("Frequencies must be positive")
        leaf = Node(frequency, symbol)
        leaves[symbol] = leaf
        pq.update(next_key, frequency, data=leaf)
        next_key += 1

    if pq.count() == 0:
        return Codec(None, leaves)

    while pq.count() > 1:
        # Peek, fetch its node, then remove it for two min items
        first_key = pq.peek_min()
        first = pq.get_data(first_key)
        pq.remove(first_key)

        second_key = pq.peek_min()
        second = pq.get_data(second_key)
        pq.remove(second_key)

        parent = Node(first.frequency + second.frequency) #sum of two mins
        parent.left = first
        parent.right = second
        first.parent = parent
        second.parent = parent

        pq.update(next_key, parent.frequency, data=parent)
        next_key += 1

    root = pq.get_data(pq.peek_min()) #we exit the loop once the pq count is not more than 1 so it becomes the root
    return Codec(root, leaves)
