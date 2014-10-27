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
    self.sizeX = 200 # Km
    self.sizeY = 200 # Km
    self.age = 0
    self.asteroids = []; # Stores all asteroids that have hit
    self.craters = [];

  def crater(self, id):
    self.incrementAge()
    a = Asteroid(id,self.sizeX,self.sizeY)
    # self.asteroids.append(a)
    # If conflicting crater
    conflict = self.findConflict(a);
    if (conflict != "false"):
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
    for c in self.craters:
      [ax,ay] = a.location
      [cx,cy] = c.location
      
      # Find out if ax, ay is within a crater
      if ((ax - cx)**2 + (ay - cy)**2 <= (c.impactDiameter/2)**2):
        # Return conflicting crater
        # print("Conflict found, returning crater");
        return c
    # Otherwise return false, no conflict found
    return "false";
       
  def numCraters(self):
    return len(self.craters);

  def plotAdd(self,c):
    (x,y) = c.location
    plot(x,y,'bo')
    
    
  def plotAll(self):
    fig = gcf()
    ax = gca()
    ax.cla()
    ax.set_xlim((0,self.sizeX))
    ax.set_ylim((0,self.sizeY))
    for c in self.craters:
        (cx,cy) = c.location
        circle=Circle((cx,cy),c.diameter/2,color='b',fill=False)
        fig.gca().add_artist(circle)
        circle2=Circle((cx,cy),1,color='black',fill=False)
        fig.gca().add_artist(circle2)
    


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

while (i < 30000000):
    s.crater(i);
    numCraterList.append(s.numCraters())
    pctg = ((numCraterList[i] -numCraterList[int(i/2)])/float(numCraterList[i]));
    # print(pctg)
    if(pctg < .05 and i > 1000):
        print("Found Equilibrium"); 
        print(numCraterList[int(i/2)])
        break;
    else:
        i = i + 1;

    
s.plotAll();

#for i in range(0,1000):
#    s.crater(i)
#print(s.numCraters())
#s.plotAll()