# Author: Brian Newsom
# Date: 10/14/14
# Program to simulate cratering on a theoretical region for
#   the class ASTR 3750: Planets, Moons, and Rings.

from matplotlib.pyplot import *
import random
import math;

class Surface:
  # Class: Maintains the state of the surface simulated, storing every crater 
  #  and every asteroid that has hit it.
  def __init__(self):
    self.sizeX = 500 # Km
    self.sizeY = 500 # Km
    self.age = 0
    self.asteroids = []; # Stores all asteroids that have hit
    self.craters = [];

  def crater(self, id):
    # Simulates crater hitting planet
    self.incrementAge()
    a = Asteroid(id,self.sizeX,self.sizeY)
    # Find all conflicts
    conflicts = self.findConflict(a);
    # If any, remove all conflicts (not just one)
    if (conflicts):
      for conflict in conflicts:
        self.craters.remove(conflict)
    # Regardless, append new crater
    self.craters.append(a);

  def incrementAge(self):
    # Increments age of surface by 1000 years
    self.age = self.age + 1000

  def printAsteroids(self):
    # Prints all asteroids that have hit the surface (some may be obliterated)
    if not self.asteroids:
      print("No asteroids present yet!");
    else:
      for a in self.asteroids:
        print("Asteroid " + str(a.id) + " At location " + str(a.location))

  def printCraters(self):
    # Print all craters currently present on surface
    if not self.craters:
      print("No craters present yet!");
    else:
      for c in self.craters:
        print("Crater " + str(c.id) + " At location " + str(c.location))

  def findConflict(self,a):
    # Given asteroid a, finds craters on surface that will be obliterated by a
    conflicts = [];
    for c in self.craters:
      [ax,ay] = a.location
      [cx,cy] = c.location
      
      # If crater is inside of impact diameter of a it is a conflict
      if ((ax - cx)**2 + (ay - cy)**2 <= (c.impactDiameter/2)**2):
        conflicts.append(c);
    # Return list of craters to be obliterated (empty list is okay)
    return conflicts;
    
  def printInfo(self):
    # Print all relevant info for the surface
    print("Surface size is " + str(self.sizeX) + " km by " + str(self.sizeY)+ \
        " km.");
    print("Surface is " + str(self.age) + " years old.")    
    self.printAsteroids();
    self.printCraters();
    return;
    
       
  def numCraters(self):
    # Simply returns the number of craters currently on surface
    return len(self.craters);

  def plotAdd(self,c):
    # plot individual crater on surface figure
    (x,y) = c.location
    plot(x,y,'bo')
    
    
  def plotAll(self, years, numCraters):
    # Plot all craters on surface at given time in years and the number of 
    #   craters
    fig = figure();
    # Setup axes and labels
    ax = gca()
    ax.cla()
    ax.set_xlim((0,self.sizeX))
    ax.set_ylim((0,self.sizeY))
    ax.set_title("Surface after " + str(years) + " years with " + \
      str(numCraters) + " craters")
    ax.set_xlabel('X Location')
    ax.set_ylabel('Y Location')
    
    # Plot each crater
    for c in self.craters:
        (cx,cy) = c.location
        # Center point is black
        center=Circle((cx,cy),1,color='black',fill=False)
        # Obliterated area is red
        areaObliterated=Circle((cx,cy),c.impactDiameter/2,color='r',fill=False)
        # Crater size is blue
        craterSize=Circle((cx,cy),c.diameter/2,color='b',fill=False)
        # Add all to plots
        fig.gca().add_artist(center)        
        fig.gca().add_artist(areaObliterated)
        fig.gca().add_artist(craterSize)


class Asteroid:
  # Class defines each asteroid that contacts planet 
  def __init__(self, id, sizeX, sizeY):
    self.id = id
    self.diameter = 50 # Kilometers
    self.impactDiameter = 60 # Kilometers
    self.impact(sizeX,sizeY);
    
  # Generates random integer location x and y for asteroid to hit a planet
  def impact(self,sizeX,sizeY):
    impactX = random.randint(0,sizeX);
    impactY = random.randint(0,sizeY);
    self.location = [impactX, impactY]

def plotCratersVsTime(numCraterList, timeToEq):
    time = len(numCraterList);
    fig = figure();
    # Setup axes and labels
    ax = gca()
    ax.cla()
    ax.set_xlim((0,time))
    ax.set_ylim((0,max(numCraterList)))
    ax.set_title("Number of Craters vs. Time (Red Circle Denotes Saturation \
      Equilibrium)")
    ax.set_xlabel('Time (In 1000 Years)')
    ax.set_ylabel('Number of Craters On Surface')
    
    # Plot each number of craters at each time
    for i in range(0,time):
        point=Circle((i,numCraterList[i]),1,color='b',fill=False)
        fig.gca().add_artist(point)
    
    # Add red circle for equilibrium point
    eq=Circle((timeToEq,numCraterList[timeToEq]),5,color='r',Fill=False)
    fig.gca().add_artist(eq)

def tableCratersVsTime(numCratersList, timeToEq):
    # Function to create table of time and number of craters
    print("---------Table of Number of Craters vs. Time------------------");
    print("Time Passed" + "\t" + "Number of Craters on Surface")
    # Prepend time = 0 and number of craters 0
    print("0" + "\t\t" + "0")
    # Print out each number
    for i in range(0,len(numCratersList)):
        print(str((i+1)*1000) + "\t\t" + str(numCratersList[i]))

if __name__ == "__main__":
    # Create a surface to run simulation on, print info to ensure correctness
    s = Surface();
    s.printInfo();
    # Holds number of craters present at each time of interest
    numCraterList = [];
    # Define constants for simulation
    iter = 0;
    maxIter = 10000;
    minToEq = 100;
    plotTimes = [1,10,100,250,400];
    yearsPassed = 0;
    eqPctg = .05;
    print("Running Simulation");
    # While within reasonable number of iterations (to ensure we don't run
    #   forever)
    while (iter < maxIter):
        # Allow asteroid to hit planet
        s.crater(iter);
        numCraterList.append(s.numCraters())
        # Determine change in number of craters from half current time
        pctg = math.fabs(((numCraterList[iter] - numCraterList[int(iter/2)])/ \
          float(numCraterList[iter])));
        
        # If we put time in plotTimes, plot the current state of surface for
        #   Extra Credit
        if (iter+1) in plotTimes:
          s.plotAll(s.age,numCraterList[iter])
           
        # If pctg is less than the desired to reach saturation equilibrium  
        if(pctg < eqPctg and iter > minToEq):
            print("After " + str(s.age) + " years, the number of craters is \
              only " + str(numCraterList[iter]) + ", differing from half of \
              the time (" + str(s.age/2) + " years) by only " + \
              str(pctg*100)[:3] + "%.")
            print("Found Saturation equilibrium at " + \
              str(numCraterList[int(iter/2)]) + " craters at " + \
              str(int(iter/2)*1000) + " years."); 
            plotCratersVsTime(numCraterList,int(iter/2))
            tableCratersVsTime(numCraterList,int(iter/2))
            break;
        # Otherwise increment iterations
        else:
            iter = iter + 1;

