# Author: Brian Newsom
# Date: 10/14/14
# Program to simulate cratering on a theoretical region for
#   the class ASTR 3750: Planets, Moons, and Rings.
# Work in progress.

from pylab import *
import random
import math


class Surface:
  def __init__(self):
    self.sizeX = math.ceil(math.sqrt(500)) # Km
    self.sizeY = math.ceil(math.sqrt(500)) # Km
    self.age = 0
    self.asteroids = []; # Stores all asteroids that have hit
    self.craters = [];

  def crater(self, id):
    self.incrementAge()
    a = Asteroid(id,self.sizeX,self.sizeY)
    self.asteroids.append(a)
    # If conflicting crater
    conflict = self.findConflict(a);
    if (conflict != "false"):
      # Remove old crater
      self.craters.remove(conflict)
      self.plotRemove(conflict)
      #print("Crater Removed");
    # Regardless, append new crater
    self.craters.append(a);
    self.plotAdd(a)
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
    plot(x,y,'b+')
    
  def plotRemove(self,c):
    (x,y) = c.location
    plot(x,y,'w+')
        
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

#while (1==1 and i < 10):
#  s.crater(i);
#  numCraterList.append(s.numCraters())
#  if(((numCraterList[i] -numCraterList[math.floor(i/2)])/numCraterList[i]) < 1.05):
#    print(numCraterList[i]);
#  i = i + 1;
figure()
for i in range(0,1000):
    s.crater(i)
print(s.numCraters())