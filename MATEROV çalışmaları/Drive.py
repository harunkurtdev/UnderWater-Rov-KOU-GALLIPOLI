#import statments
import math
import numpy as np
import random
#user input from 1 to -1
#define globals
#x goes first then y and then z in coordiantes
fn = [1 for i in range(0,6)]
cG = [0,0,0]
locations = [[5,-4,0],
             [5,4,0],
             [-5,4,0],
             [-5,-4,0],
             [4,0,0],
             [-4,0,0]]
thetan = [(math.pi)/9.0 for i in range(0,6)]
alphan = [(8.11 * math.pi)/180.0 for i in range(0,6)]
acoe = [[0 for i in range(0,6)] for j in range(0,6)]
fsigns = [[1,1,1],[1,-1,-1],[1,1,1],[1,-1,-1],[0,0,1],[0,0,1]]
#calculate the unit force that the motor exerts in respect to the center of gravity
def calculateforces(n):
    tnx = fsigns[n][0] * fn[n] * math.cos(thetan[n])
    tny = fsigns[n][1] * fn[n] * math.sin(thetan[n])
    tnz = fsigns[n][2] * fn[n] * math.tan(alphan[n])
    lengthn = math.sqrt(tnx ** 2 + tny ** 2 + tnz ** 2)
    v = [tnx/lengthn,tny/lengthn,tnz/lengthn]
    return v

#Calculating the radius of the motor from the center of gravity
def calulaterTn(n):
    x = locations[n][0] - cG[0]
    y = locations[n][1] - cG[1]
    z = locations[n][2] - cG[2]
    b = [x,y,z]
    return b

#Calculate torque given the vectors of radius and force
def Torque(radius,force):
    aTx = (radius[1] * force[2] - radius[2] * force[1])
    aTy = (radius[2] * force[0] - radius[0] * force[2])
    aTz = (radius[0] * force[1] - radius[1] * force[0])
    return [aTx,aTy,aTz]

#Update the values of coefficents in our 6 equations
def updatecoefficents():
    for i in range(0,6):
        currentforce = calculateforces(i)
        for j in range(0,3):
            acoe[j][i] = currentforce[j]
        currenttorque = Torque(calulaterTn(i),currentforce)
        for j in range(3,6):
            acoe[j][i] = currenttorque[j - 3]
            
#Solve the linear equation for user input using Gaussian elimination
def solvelinearequation(answers):
    if(len(acoe) == len(answers)):
        return np.linalg.solve(acoe,answers)
    else:
        return -1
#Print array of coefficents
def printacoe():
    for i in range(0,6):
        v = ""
        for j in range(0,6):
            v += str(round(acoe[i][j],3)) + " "
        print(v)
#Print the given array rounded to n decimal places
def arrayrounded(y,n):
    v = ""
    for i in range(0,len(y)):
        v += str(round(y[i],n)) + " "
    return v
#Adjust the raw solutions to be betweeen -250 and 250
def adjustmotorvalues(motor):
    r = []
    max = math.fabs(motor[0])
    for i in range(0,len(motor)):
        if(motor[i] == 0.0):
            r.append(0.0)
        else:
            r.append(motor[i])
        v = math.fabs(motor[i])
        if(v > max):
            max = v        
    if(max > 1):
        for i in range(0,len(r)):
            r[i] = r[i]/max    #convert the decimals to percent
    #for i in range(0,len(r)):
           # r[i] = 100.0 * r[i]
    return r
#User calls the method to get the solution
def getsolution(y):
    return arrayrounded(solvelinearequation(y),3)

updatecoefficents()
x = [0.1,1,0,0,2,0]
print(getsolution(x))
