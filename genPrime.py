#!/usr/bin/python
'''
  genPrime

'''
import sys
import random

def is_even(n):
    '''
    the function check n is even or not
    :param n: the number being tested
    :return: True or False
    Time complexity: O(1)
    '''
    if n % 2 == 0:
        return True
    return False

# Input: n > 2, is the number being tested for primality
# Input: k, a parameter that determines accuracy of the test
def miller_rabin_test(n, k = 5):
    '''
    the function run miller-rabin algorithm to test whether n is prime or not
    :param n: the number being tested
    :param k: the parameter that determines accuracy of the test
    :return: True or False
    Time complexity: O(k*log(n))
    '''
    if is_even(n):
        return False
    s = 0
    t = n - 1
    while is_even(t):
        s = s + 1
        t = t / 2
    # at this stage , n-1 will be 2^s.t, where t is odd
    while k > 0:
        a = random.randint(2, n - 1) #[2...n-1]
        if pow(a, n-1, n) != 1:
            return False
        for i in range(1, s + 1): #[1...s]
            tmp1 = pow(2, i) * t
            tmp2 = pow(2, i-1) * t
            if pow(a, tmp1, n) == 1 and abs(pow(a, tmp2, n)) != 1:
                return False
        k = k - 1
    return True


if len(sys.argv) < 2:
    print("please check args.")
else:
    m = int(sys.argv[1])
    # [2^(m-1), 2^m -1]
    low = pow(2, m - 1)
    high = pow(2, m) -1
    while True:
        n = random.randint(low, high)
        if miller_rabin_test(n):
            print(n)
            break
        #break
