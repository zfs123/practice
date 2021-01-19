# practice

#### Miller-Rabin algorithm
Program name: `genPrime.py`
Argument to your program: `m`
Command line usage of your script: `genPrime.py <m>`
Output: Output to terminal the value of prime `n` in decimal (which would take m-bits to represent in binary).
Example: m = 4, the program will output either 11 or 13.

#### Huffman algorithm
Program name: `header.py`
Argument to your program: An input text file containing a string str[0 . . . nn1]. It is safe to assume that:
- str consists of ASCII characters (characters are not restricted to be lower case
only!).
- There are no line breaks in the input file.

Command line usage of your script: `header.py <input text file>`
Output format: The output is a text file containing a header for the input string str. The header is a bitstring (see the note above which details how to represent the bits) made up of the following information:
 - The number of unique ASCII characters in str encoded using the corresponding
Elias ω integer code.
 - For each unique character in the text:
   - Encode the unique character using the fixed-length 7-bit ASCII code. (All
input characters will have ASCII values < 128).
   - Then encode the length of the Huffman code assigned to that unique character using an Elias ω code.
   - To the above, append the variable-length Huffman codeword assigned to that unique character.

Example：`aacaacabcaba ==》011110000111110001001000110001101001`

#### Lempel-Ziv-Storer-Szymanski (LZSS) decoder
a variation of the LZ77 algorithm.

Example: 
```
01111000011111000100100011000110100100011111111010011000100100001101111
===>
aacaacabcaba
```