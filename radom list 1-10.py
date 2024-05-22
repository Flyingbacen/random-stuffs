from random import *
from time import * 
this=False
x=0
TimeStart=time()
while this==False:
    x+=1
    abc=sample(range(1, 11), 10)
    if sorted(abc) == list(range(1, 11)):
        this=True
        print(f"{abc}\nthis took {x} tries and {time()-TimeStart} seconds\nthis has a chance of 1 in {10**10}")