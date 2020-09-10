#Exact same as the Drive code but in a class to that it can be easily called by other programs

#import statments
import math
import numpy as np
import random
#user input from 1 to -1
#define globals
#x goes first then y and then z in coordiantes
class Drive:
    cG = [0,0,0]
    locations = [[9,19.5,0],[-9,19.5,0],[-9,-19.5,0],[9,-19.5,0],[9,0.01,0],[-9,-0.01,0]]
    thetan = [(20 * math.pi)/180.0 for i in range(0,6)] #Toe
    alphan = [(0.01 * math.pi)/180.0 for i in range(0,6)] #Lateral 
    acoe = [[0 for i in range(0,6)] for j in range(0,6)]
    fsigns = [[1,1,1],[1,-1,-1],[1,1,1],[1,-1,-1],[0,0,1],[0,0,1]]
    total = [0 for i in range(0,6)]
    #calculate the unit force (Page 2 - 3) in document
    
    def calculateforces(s,n):
        tnx = s.fsigns[n][0] * math.cos(s.thetan[n])
        tny = s.fsigns[n][1] * math.sin(s.thetan[n])
        tnz = s.fsigns[n][2] * math.tan(s.alphan[n])
        lengthn = math.sqrt(tnx ** 2 + tny ** 2 + tnz ** 2)
        return [tny/lengthn,tnx/lengthn,tnz/lengthn]

    #Calculating the radius needed for the cross product
    def calulaterTn(s,n):
        x = s.locations[n][0] - s.cG[0]
        y = s.locations[n][1] - s.cG[1]
        z = s.locations[n][2] - s.cG[2]
        return [y,x,z]

    #Calculate torque given the vectors of radius and force
    def Torque(s,radius,force):
        aTx = (radius[1] * force[2] - radius[2] * force[1])
        aTy = (radius[2] * force[0] - radius[0] * force[2])
        aTz = (radius[0] * force[1] - radius[1] * force[0])
        return [aTy,aTx,aTz]

    #Update the values in the a table
    def updatecoefficents(s):
        for i in range(0,6):
            currentforce = s.calculateforces(i)
            for j in range(0,3):
                s.acoe[j][i] = currentforce[j]
            currenttorque = s.Torque(s.calulaterTn(i),currentforce)
            for j in range(3,6):
                s.acoe[j][i] = currenttorque[j-3]
        for i in range(0,6):
            tot = 0.0
            for j in range(0,6):
                tot += abs(s.acoe[i][j])
            s.total[i] = tot
        s.total[3] *= 0.5
        

    def solvelinearequation(s,answers):
        if(len(s.acoe) == len(answers)):
            return np.linalg.solve(s.acoe,answers)
        raise SystemExit(0)

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
        maxv = math.fabs(motor[0])
        for i in range(0,len(motor)):
            r.append(motor[i])
            v = abs(motor[i])
            if(v > maxv):
                maxv = v
        maxv = max(maxv,1)
        for i in range(0,len(r)):
            r[i] = (r[i]/maxv) ** 3
            r[i] = int(250.0 * r[i])
        return r
              
    def getsolution(s,y):
         for i in range(0,6):
             if(abs(y[i]) < 0.1):
                 y[i] = 0
             y[i] *= s.total[i]
         v = s.solvelinearequation(y)
         #return v
         return s.adjustmotorvalues(v)
         #return s.arrayrounded(v,3)
        
t1 = Drive()
t1.updatecoefficents()
#print(t1.total)
#t1.printarray()
j = -1.0
while(j <= 1.0):
    x = [0 for i in range(0,6)]
    x[1] = j
    print("Power of " + str(j) + ": " + str(t1.getsolution(x)))
    j += 0.25
