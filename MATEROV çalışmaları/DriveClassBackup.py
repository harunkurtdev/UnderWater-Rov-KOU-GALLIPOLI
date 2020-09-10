#import statments
import math
import numpy as np
import random
#user input from 1 to -1
#define globals
#x goes first then y and then z in coordiantes
class Drive:
    a = 0.342
    b = 0.940
    c = 0.002
    d = 0.034
    e = 0.016
    f = 15.127
    acoe = [[-a,a,-a,a,0,0],
            [b,b,b,b,0,0],
            [c,-c,c,-c,1,1],
            [d,-d,-d,d,0.001,-0.001],
            [-e,-e,e,e,-9,9],
            [f,-f,-f,f,0,0]]
    sums = [4 * a,4 * b, 3 * c + 2,4 * d + 0.002, 4 * e + 18, 4 * f]
    def solvelinearequation(s,answers):
        if(len(s.acoe) == len(answers)):
            return np.linalg.solve(s.acoe,answers)
        else:
            print("Error")

    def printarray(s):
        for i in range(0,6):
            v = ""
            for j in range(0,6):
                v += str(round(s.acoe[i][j],3)) + " "
            print(v)

    def arrayrounded(s,y,n):
        v = ""
        for i in range(0,len(y)):
            v += str(round(y[i],n)) + " "
        return v

    def adjustmotorvalues(s,motor):
        r = []
        maxv = abs(motor[0])
        for i in range(0,len(motor)):
            r.append(motor[i])
            v = abs(motor[i])
            if(v > maxv):
                maxv = v
        maxv = max(maxv,1)
        for i in range(0,len(r)):
            r[i] = r[i]/maxv
            r[i] = int(250.0 * r[i])
            if(abs(r[i]) < 25):
                r[i] = 0
        return r
              
    def getsolution(s,y):
        for i in range(0,len(y)):
            y[i] *= s.sums[i]
        v = s.solvelinearequation(y)
        return s.adjustmotorvalues(v)

t1 = Drive()
print(t1.acoe)
x = [0.9,0.5,0,0,0,0]
print(t1.getsolution(x))
