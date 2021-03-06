#!/usr/bin/env python

# ============================================================================ #

import sys
import time

# ============================================================================ #

FILE_AIRPORTS = 'data/airports.txt' 
FILE_ROUTES = 'data/routes.txt'

DAMPING_FACTOR = 0.85   # between 0 and 1 (normally between 0.8 and 0.9)
DECIMAL_VALUE = 10**(-12)

# ============================================================================ #

class Route:

    def __init__ (self, origin=None, index=None):
        
        self.origin = origin
        self.index = index
        self.weight = 1.0

    def __repr__(self):
        
        return '<edge: ({0}, {1})>'.format(self.origin, self.weight)

    def getOrigin(self):

        return self.origin

    def getIndex(self):
        
        return self.index

    def getWeight(self):

        return self.weight

    def increase(self):

        self.weight += 1

class Airport:

    def __init__(self, code=None, name=None, index=None):

        self.code = code
        self.name = name

        self.index = index

        self.routes = []
        self.routeHash = dict()
        
        self.outweight = 0.0
    
    def __repr__(self):
        
        return '<airport: ({0}, {1})>'.format(self.code, self.name)
    
    def getCode(self):

        return self.code

    def getName(self):

        return self.name

    def getIndex(self):

        return self.index

    def getRoutes(self):

        return self.routes

    def getRouteHash(self):

        return self.routeHash

    def getOutweight(self):

        return self.outweight

    def addRoute(self, codeO):

        if codeO in self.routeHash:
            route = self.routes[self.routeHash[codeO]]
            route.increase()

        else:
            route = Route(codeO, airportHash[codeO].index)
            
            routeList.append(route)
            routeHash[codeO] = route
            
            self.routes.append(route)
            self.routeHash[codeO] = len(self.routes) - 1

    # debug function in case we need to print airport attributes
    def print(self):

        print('Airport:')
        print('  - code:', self.code)
        print('  - name:', self.name)
        print('  - routes:', self.routes)
        print('  - routeHash:', self.routeHash)
        print('  - outweight:', self.outweight)

# ============================================================================ #

routeList = []          # list of Route
routeHash = dict()      # hash of Route to ease the match

airportList = []        # list of Airport
airportHash = dict()	# hash key IATA code -> Airport

# ============================================================================ #

def printMsg(msg):
    
    print('[pagerank]', msg)

def getAirport(code):

    if not code in airportHash:
        raise Exception ("Airport not found.")
    
    return airportList[airportHash[code].index] 

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
            
            airport.name = temp[1][1:-1] + ", " + temp[3][1:-1]
            airport.code = temp[4][1:-1]
            airport.index = count
        
        except Exception:
            pass
        
        else:
            count += 1
            airportList.append(airport)
            airportHash[airport.code] = airport
    
    airportsTxt.close()
    
    printMsg('read '+str(count)+' aiports with IATA code') # VERBOSE

def readRoutes(file):

    printMsg('reading routes from '+file) # VERBOSE

    routesTxt = open(file, "r")

    count = 0
    for line in routesTxt.readlines():
        
        try:
            route = line.split(',')

            codeO = route[2]
            codeD = route[4]

            if len(codeO) != 3 or len(codeD) != 3:
                raise Exception('not an IATA code')

            airpO = getAirport(codeO)
            airpD = getAirport(codeD)

            airpO.outweight += 1.0
            airpD.addRoute(codeO)
        
        except Exception:
            pass
        
        else:
            count += 1

    routesTxt.close()

    printMsg('read '+str(count)+' routes with IATA codes')

def computePageRanks():

    printMsg('computing pagerank') # VERBOSE

    # here we apply statement's pseudocode

    n = len(airportList)
    P = [1.0/n] * n
    L = DAMPING_FACTOR

    nO = len(list(filter(lambda n: n.outweight == 0.0, airportList)))
    numOut = L/float(n-1) * nO
    aux = 1.0/n

    iters = 0
    stop = False

    while not stop:
        Q = [0.0] * n

        for i in range(n):
            airport = airportList[i]
            
            summation = 0
            for route in airport.routes:
                index = route.index
                weight = route.weight
                outweight = airportList[index].outweight
                summation += P[index]*weight / outweight

            Q[i] = L*summation + (1.0-L)/n + numOut*aux

        aux = (1.0-L)/n + numOut*aux

        value = [a - b for a, b in zip(P, Q)]
        absVal = map(lambda val: abs(val), value)
        stop = all(map(lambda val: val < 1 * DECIMAL_VALUE, absVal))

        P = Q
        iters += 1
    
    global pageRank
    pageRank = P.copy()
    return iters

def outputPageRanks():
    
    printMsg('printing pagerank results: (pagerank, airport name)')

    ls = []
    i = 0
    for k in airportHash:
        a = airportHash[k]
        x = (pageRank[i], a.name)
        ls.append(x)
        i += 1
        
    ls.sort(key=lambda x: x[0], reverse=True)

    s = '============================================================================\n'
    for (x,y) in ls:
        s += ("(%s : %s)\n"%(x, y))
    s += '============================================================================'
    print(s)

# ============================================================================ #

def main(argv=None):

    readAirports(FILE_AIRPORTS)
    readRoutes(FILE_ROUTES)
    
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    
    printMsg('iterations done: '+str(iterations))
    printMsg('time spent: '+str(time2-time1))

if __name__ == "__main__":
    
    sys.exit(main())
