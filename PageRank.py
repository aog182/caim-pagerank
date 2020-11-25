#!/usr/bin/env python

# ============================================================================ #

from collections import namedtuple
import sys
import time

# ============================================================================ #

FILE_AIRPORTS = 'data/airports.txt' 
FILE_ROUTES = 'data/routes.txt'

# ============================================================================ #

class Edge:

    def __init__(self, origin=None):

        self.origin = 0 # ADJUSTABLE
        self.weight = 0 # ADJUSTABLE

    def __repr__(self):

        return "edge: {0} {1}".format(self.origin, self.weight)


class Airport:

    def __init__(self, iden=None, name=None):

        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0 # ADJUSTABLE
    
    def __repr__(self):
        
        return f"{self.code}\t{self.pageIndex}\t{self.name}"
    
    def getCode(self):
        
        return self.code
    
    # debug function in case we need to print airport attributes
    def print(self):

        print('Airport:')
        print('  - code:', self.code)
        print('  - name:', self.name)
        print('  - routes:', self.routes)
        print('  - routeHash:', self.routeHash)
        print('  - outweight:', self.outweight)

# ============================================================================ #

edgeList = []           # list of Edge
edgeHash = dict()       # hash of edge to ease the match

airportList = []        # list of Airport
airportHash = dict()	# hash key IATA code -> Airport

# ============================================================================ #

def printMsg(msg):
    
    print('[pagerank]', msg)


def readAirports(file):

    printMsg('reading airports from '+file) # VERBOSE
    
    airportsTxt = open(file, "r")
    
    count = 0
    for line in airportsTxt.readlines():
        airport = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            airport.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            airport.code=temp[4][1:-1]
        
        except Exception as inst:
            pass
        
        else:
            count += 1
            airportList.append(airport)
            airportHash[airport.code] = airport
    
    airportsTxt.close()
    
    printMsg('read '+str(count)+' aiports with IATA code') # VERBOSE


def readRoutes(file):
    pass


def computePageRanks():
    pass


def outputPageRanks():
    pass

# ============================================================================ #

def main(argv=None):

    readAirports(FILE_AIRPORTS)
    readRoutes(FILE_ROUTES)

    airportList[0].print() # DEBUG
    airportHash[airportList[0].code].print() # DEBUG
    
    sys.exit(0) # DEBUG
    
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    
    sys.exit(main())
