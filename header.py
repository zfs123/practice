#!/usr/bin/python

import sys

def components(c):
    '''
    the function encodes components
    :param c: the component to be encode
    :return: the encoded string
    Time complexity: O(log(c))
    '''

    if c < 1:
        return ""

    result = ""
    bitc = bin(c)[3:]

    # change the first bit to "0"
    bitc = "0" + bitc
    bit_len = len(bitc) - 1
    result = result + components(bit_len) + bitc
    return result

def elias(n):
    '''
    the function start Elias(omega) encode
    :param n: the number being encoded
    :return: the encoded string
    Time complexity: O(log(n))
    '''
    if n == 1:
        return "1"
    bitn = bin(n)[2:]
    return components(len(bitn) - 1) + bitn


def count_unique_char(string):
    '''
    the function count the number of the unique characters and occur times
    :param string: the input string
    :return: {char: occur_times}, the number of the unique characters
    Time complexity: O(N), N is length of the string
    '''
    result = {}
    count = 0
    
    for i in range(len(string)):
        c = string[i]
        if not result.has_key(c):
            result[c] = string.count(c)
            count = count + 1
    
    return result, count


class Node:
    '''
    huffman node class, used to build huffman tree
    '''
    def __init__(self, char, occur_times):
        '''
        the function create a huffman node
        :param char: node's character
        :param occur_times: character occurs times
        '''
        self.char = char
        self.occur_times = occur_times
        self.left = None
        self.right = None
        self.father = None

    def is_right(self):
        '''
        this function check the node in right or not
        :return: True or False
        '''
        return self.father.right == self


def huffman(chars):
    '''
    the function compute huffman code for char in chars
    :param chars: dict{char: times}, character and occurs times
    :return: dict{char, huffman_code}, character and huffman codeword
    Time complexity: O(N), N is the number of unique characters
    '''
    huffman_node = []
    for k, v in chars.items():
        huffman_node.append(Node(k, v))
    
    tree = huffman_node[:]
    while True:
        if len(tree) <= 1:
            break
        tree.sort(key=lambda item: item.occur_times)
        l = tree.pop(0)
        r = tree.pop(0)
        f = Node(None, l.occur_times + r.occur_times)
        f.left = l
        f.right = r
        l.father = f
        r.father = f
        tree.append(f)
    tree[0].father = None

    node_len = len(huffman_node)
    result = {}
    result_code = [''] * node_len
    
    for i in range(node_len):
        node = huffman_node[i]
        char = node.char
        while node != tree[0]:
            if node.is_right():
                result_code[i] = '1' + result_code[i]
            else:
                result_code[i] = '0' + result_code[i]
            node = node.father
        
        result[char] = result_code[i]
    return result
    
def ascii(c):
    '''
    the function compute ASCII code(<128) for char c.
    :param: c, the char being encoded
    :return: the encoded string, length is 7.
    Time complexity: O(1)
    '''
    binc = bin(ord(c))[2:]
    left = 7 - len(binc)
    result = binc
    while left > 0:
        result = "0" + result
        left = left - 1
    return result

def run():
    '''
    the function is entry function.
    '''
    if len(sys.argv) < 2:
        print("please check args.")
    else:
        inputfile = sys.argv[1]
        with open(inputfile, "r") as fin:
            string = fin.read()
            chars, count = count_unique_char(string)
            pre = elias(count)
            char_codes = huffman(chars)
            
            result = pre
            for k in sorted(chars.keys()):
                ascii_code = ascii(k)
                char_code = char_codes[k]
                char_code_len_elias = elias(len(char_code))
                result = result + ascii_code + char_code_len_elias + char_code
        
        with open("output_header.txt", "w") as fout:
            fout.write(result)
                
if __name__ == '__main__':
    run()
