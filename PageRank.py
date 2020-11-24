#!/usr/bin/env python

# ============================================================================ #

from collections import namedtuple
import time
import sys

# ============================================================================ #

class Edge:

    def __init__(self, origin=None):
        self.origin = 0 # write appropriate value
        self.weight = 0 # write appropriate value

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
    
    # TODO #


class Airport:

    def __init__(self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0 # write appropriate value
        
    def __repr__(self):
        return f"{self.code}\t{self.pageIndex}\t{self.name}"
    
    # airport code getter
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
        
    # TODO #

# ============================================================================ #

edgeList = []           # list of Edge
edgeHash = dict()       # hash of edge to ease the match
airportList = []        # list of Airport
airportHash = dict()    # hash key IATA code -> Airport

# ============================================================================ #

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print(f"There were {cont} Airports with IATA code")


def readRoutes(fd):
    print("Reading Routes file from {fd}")
    routesTxt = open(fd, "r")
    cont = 0
    for line in routesTxt.readLines():
        try:
            tmp = line.split(',')
            # TODO #
    return


def computePageRanks():
    return


def outputPageRanks():
    return

# ============================================================================ #

def main(argv=None):

    readAirports("airports.txt")
    # readRoutes("routes.txt")
    
    sys.exit(0)
    
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())
