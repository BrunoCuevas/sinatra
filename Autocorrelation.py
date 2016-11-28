from numpy import *
import numpy as N
import pylab as P

fn = 'data.txt'
x = loadtxt(fn,unpack=True,usecols=[1])
time = loadtxt(fn,unpack=True,usecols=[0]) 

def estimated_autocorrelation(x):
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = N.correlate(x, x, mode = 'full')[-n:]
    #assert N.allclose(r, N.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(N.arange(n, 0, -1)))
    return result

P.plot(time,estimated_autocorrelation(x))
P.xlabel('time (s)')
P.ylabel('autocorrelation')
P.show()
