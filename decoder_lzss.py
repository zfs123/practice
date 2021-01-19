#!/usr/bin/python

import sys


def elias_decode(code_string, cpt_len = 0):
    '''
    the function decode elias code string
    :param:codestring, the code string being decoded
    :param:cpt_len, length of next component
    :return: decoded number and length of elias code
    Time complexity: O(log(N)), N is the length of string
    '''
    sum_length = 0
    if code_string[0] == "1": # number
        return int(code_string[:cpt_len+1], 2), cpt_len + 1
    
    # component, change the first bit to 1
    code = "1" + code_string[1:]
    length = int(code[:cpt_len+1], 2)

    left = code_string[cpt_len+1:]
    if len(left) == 0:
        return length, cpt_len + 1
    else:
        sum_length = cpt_len + 1
        result, sub_length = elias_decode(left, length)
        sum_length += sub_length
        return result, sum_length

def ascii_to_char(code):
    '''
    the function convert ASCII code to char
    :param: code, code being coverted
    :return: char
    Time complexity: O(1)
    '''
    dec = int(code, 2)
    return chr(dec)

class Format01:
    '''
    the class is used to represent Format-0/1 fields 
    '''
    def __init__(self, btype, param1, param2 = None):
        self.btype = btype
        self.data1 = param1
        self.data2 = param2


def find_char(char_codes_dict, s):
    '''
    the function return a char whose huffman code is prefix of s
    :param: char_codes_dict, dict{char: huffman_code}
    :param: s, string
    :return: a char whose huffman code is prefix of s
    Time complexity: O(N), N is the number of dict items.
    '''
    for k, v in char_codes_dict.items():
        if v == s[:len(v)]:
            return k


def lzss_decode(format01_list):
    '''
    the function decodes data compressed with lzss algorithm.
    :param: format01_list, the list of Format-0/1 fields.
    :return: the data string decoded
    Time complexity: O(N*M), N is the size of list, and M is the size of window.
    '''
    result = ""
    for item in format01_list:
        # check bit type
        if item.btype == "1": # char
            result += item.data1
        elif item.btype == "0": # offset, length
            pos = len(result) - item.data1
            length = item.data2
            while length > 0:
                   result += result[pos]
                   pos = pos + 1
                   length = length -1
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
            s = fin.read()
            # decode header
            unique_chars_number, elias_code_len = elias_decode(s)
            huffman_char_codes = {}

            idx = elias_code_len
            for i in range(unique_chars_number):
                # ascii code
                char = ascii_to_char(s[idx:idx+7])

                # huffman code
                idx = idx + 7
                huffman_len, code_len = elias_decode(s[idx:])
                
                idx += code_len
                huffman_code = s[idx:idx+huffman_len]
                
                huffman_char_codes[char] = huffman_code
                idx += huffman_len

            # decode data
            format_number, number_len = elias_decode(s[idx:])
            idx += number_len
            format01_list = []
            for i in range(format_number):
                if s[idx] == "1":
                    char = find_char(huffman_char_codes, s[idx+1:])
                    format01_list.append(Format01("1", char))
                    idx = idx + len(huffman_char_codes[char]) + 1
                elif s[idx] == "0":
                    offset, offset_len = elias_decode(s[idx+1:])
                    length, length_len = elias_decode(s[idx+1+offset_len:])
                    format01_list.append(Format01("0", offset, length))
                    idx = idx + offset_len + length_len + 1
            # lzss_decode
            result = lzss_decode(format01_list)

        with open("output_decoder_lzss.txt", "w") as fout:
            fout.write(result)

if __name__ == "__main__":
    run()
