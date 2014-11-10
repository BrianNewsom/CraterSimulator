# Author: Brian Newsom
# Date: 10/14/14
# Program to simulate cratering on a theoretical region for
#   the class ASTR 3750: Planets, Moons, and Rings.
# Work in progress.

from pylab import *
from matplotlib.pyplot import *
import random
import math;

class Surface:
  def __init__(self):
    self.sizeX = 500 # Km
    self.sizeY = 500 # Km
    self.age = 0
    self.asteroids = []; # Stores all asteroids that have hit
    self.craters = [];

  def crater(self, id):
    self.incrementAge()
    a = Asteroid(id,self.sizeX,self.sizeY)
    # self.asteroids.append(a)
    # If conflicting crater
    conflicts = self.findConflict(a); # Find all conflicts
    # If any, remove them all (Not just one)
    if (conflicts):
      for conflict in conflicts:
        # Remove old crater
        self.craters.remove(conflict)
        #print("Crater Removed");
    # Regardless, append new crater
    self.craters.append(a);
    #print("Crater Added");
    #self.printCraters()

  def incrementAge(self):
    self.age = self.age + 1000

  def printAsteroids(self):
    for a in self.asteroids:
      print("Asteroid " + str(a.id) + " At location " + str(a.location))

  def printCraters(self):
    for c in self.craters:
      print("Crater " + str(c.id) + " At location " + str(c.location))

  def findConflict(self,a):
    conflicts = [];
    for c in self.craters:
      [ax,ay] = a.location
      [cx,cy] = c.location
      
      # Find out if ax, ay is within a crater
      if ((ax - cx)**2 + (ay - cy)**2 < (c.impactDiameter/2)**2):
        # Return conflicting crater
        # print("Conflict found, returning crater");
        conflicts.append(c);
    # Otherwise return false, no conflict found
    return conflicts;
       
  def numCraters(self):
    return len(self.craters);

  def plotAdd(self,c):
    (x,y) = c.location
    plot(x,y,'bo')
    
    
  def plotAll(self, years, numCraters):
    newFig = figure();
    fig = gcf()
    ax = gca()
    ax.cla()
    ax.set_xlim((0,self.sizeX))
    ax.set_ylim((0,self.sizeY))
    ax.set_title("Surface after " + str(years) + " years with " + str(numCraters) + " craters")
    ax.set_xlabel('X Location')
    ax.set_ylabel('Y Location')
    
    for c in self.craters:
        (cx,cy) = c.location
        center=Circle((cx,cy),1,color='black',fill=False)
        areaObliterated=Circle((cx,cy),c.impactDiameter/2,color='r',fill=False)
        craterSize=Circle((cx,cy),c.diameter/2,color='b',fill=False)
        # Add to plots
        fig.gca().add_artist(center)        
        fig.gca().add_artist(areaObliterated)
        fig.gca().add_artist(craterSize)


class Asteroid:
  def __init__(self, id, sizeX, sizeY):
    self.id = id
    self.diameter = 50 # Kilometers
    self.impactDiameter = 60 # Kilometers
    self.impact(sizeX,sizeY);
  def impact(self,sizeX,sizeY):
    impactX = random.randint(0,sizeX);
    impactY = random.randint(0,sizeY);
    self.location = [impactX, impactY]
    #print("crashed into point: " + str(self.location))

s = Surface();
numCraterList = [];
i = 0;
maxIter = 10000;
minToEq = 100;
plotFreq = 100;

while (i < maxIter):
    s.crater(i);
    numCraterList.append(s.numCraters())
    pctg = math.fabs(((numCraterList[i] -numCraterList[int(i/2)])/float(numCraterList[i])));
    
    if (i % plotFreq == 0):
        print("plotting");
        s.plotAll(i*1000,numCraterList[i])
        
    if(pctg < .05 and i > minToEq):
        print("Found Equilibrium at " + str(numCraterList[int(i/2)]) + " craters."); 
        break;
    else:
        i = i + 1;

    


#for i in range(0,1000):
#    s.crater(i)
#print(s.numCraters())
#s.plotAll()