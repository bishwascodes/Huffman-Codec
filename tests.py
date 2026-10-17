
import pytest
from huffman import huffman_codec


# Frequencies from Part 1
PART1 = [
    ("a", 3),
    ("b", 8),
    ("c", 10),
    ("d", 14),
    ("e", 17),
    ("f", 42)
]

#Encoding
def test_encoding_part1_total_bits():
    codec = huffman_codec(PART1)

    message = (
        "a" * 3 + "b" * 8 + "c" * 10 +
        "d" * 14 + "e" * 17 + "f" * 42
    )

    bits = list(codec.encode(message))

    # From part 1 = 209 bits
    assert len(bits) == 209


def test_encoding_part1_code_lengths():
    codec = huffman_codec(PART1)

    # Check the length of each symbol's Huffman code
    assert len(list(codec.encode("a"))) == 4
    assert len(list(codec.encode("b"))) == 4
    assert len(list(codec.encode("c"))) == 3
    assert len(list(codec.encode("d"))) == 3
    assert len(list(codec.encode("e"))) == 3
    assert len(list(codec.encode("f"))) == 1


def test_encoding_only_produces_bits():
    codec = huffman_codec(PART1)

    bits = list(codec.encode("abcdef"))

    assert set(bits) == {0, 1}


def test_encoding_single_symbol():
    codec = huffman_codec([("a", 5)])

    bits = list(codec.encode("aaa"))

    assert bits == [0, 0, 0]
    
def test_encoding_unknown_symbol():
    codec = huffman_codec([("a", 2), ("b", 3)])

    with pytest.raises(KeyError):
        list(codec.encode("abc"))
    
    
    
    
    
    
#Decoding
def test_decoding_part1():
    codec = huffman_codec(PART1)

    message = "abcdef"

    bits = list(codec.encode(message))
    decoded = list(codec.decode(bits))

    assert decoded == list(message)


def test_decoding_repeated_symbols():
    codec = huffman_codec(PART1)

    message = "aaabbccdddeefff"

    bits = list(codec.encode(message))
    decoded = list(codec.decode(bits))

    assert decoded == list(message)


def test_decoding_single_symbol():
    codec = huffman_codec([("a", 5)])

    decoded = list(codec.decode([0, 0, 0]))

    assert decoded == ["a", "a", "a"]


def test_decoding_invalid_bit():
    codec = huffman_codec(PART1)

    with pytest.raises(ValueError):
        list(codec.decode([2]))

def test_decoding_incomplete_bits():
    codec = huffman_codec(PART1)

    # Symbol 'a' has a code longer than one bit.
    bits = list(codec.encode("a"))

    # Remove the last bit to create an incomplete code.
    incomplete_bits = bits[:-1]

    with pytest.raises(ValueError):
        list(codec.decode(incomplete_bits))