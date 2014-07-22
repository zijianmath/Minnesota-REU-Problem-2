import sys
from sympy import *
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

fl = open('cyclic_pairs_data','r')
x = symbols('x')


for t in range(3):
    fl.readline()

for t in range(5):
    if t != 0:
        print t
        print poly
        print factor_list(poly)
    poly = 0
    data = fl.readline().split()
    while data[0] != 'finished':
        diff = int(data[2][:-1])
        i = int(data[1][:-1])
        n = int(data[0][1:-1])
        
        pin = nCk(n-1,i-1)-diff
        poly += pin*(x**i)


        data = fl.readline().split()

