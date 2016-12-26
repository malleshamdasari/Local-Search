import random
import sys
from collections import OrderedDict
from datetime import datetime

INF = 1000000
assignment = {}
variables = []
cons = {}
domainValues = []
ssteps = 0

def min_conflicts(max_steps):
    global variables
    global cons
    global domainValues
    global assignment
    global ssteps

    for var in variables:
        assignment[var] = random.choice(domainValues)
    curr = assignment
    def isSolution(assignment):
        for var in variables:
            for con in cons[var]:
                if assignment[var] == assignment[int(con)]:
                    return -1
        return 0
    def getRandomVariable():
        clist = []
        for var in variables:
            for con in cons[var]:
                if assignment[var] == assignment[int(con)]:
                    clist.append(var)
        return random.choice(clist)

    def getInconsistentCount(var, value):
        count = 0
        for con in cons[var]:
            if int(con) in assignment:
                if value == assignment[int(con)]:
                    count += 1
        return count
    def minConflictingValue(var, current):
        clist = {}
        for value in domainValues:
            count = getInconsistentCount(var, value)
            if count not in clist:
                clist.__setitem__(count, [])
            clist[count].append(value)
        orderedDomainValues = OrderedDict(sorted(clist.items()))
        for val in orderedDomainValues:
            orderedDomainValues[val] = sorted(orderedDomainValues[val])
        min = INF
        for key in orderedDomainValues.keys():
            if min > key:
                min = key
        return random.choice(orderedDomainValues[min])

    for step in range(max_steps):
        if isSolution(curr) == 0:
            return curr
        var = getRandomVariable()
        val = minConflictingValue(var, curr)
        ssteps += 1
        curr[var] = val
    return -1

def main(ifile, ofile):
    fh1 = open(ifile)
    fh2 = open(ofile, 'w')
    inp = []
    inp = fh1.readline().strip().split('\t')
    lines = fh1.readlines()
    global cons
    global variables
    variables = range(int(inp[0]))
    global domainValues
    domainValues = range(int(inp[2]))
    for variable in range(int(inp[0])):
        cons.__setitem__(variable, [])
    for line in lines:
        line = line.strip().split('\t')
        if line[1] not in cons[int(line[0])]:
            cons[int(line[0])].append(line[1])
        if line[0] not in cons[int(line[1])]:
            cons[int(line[1])].append(line[0])
    for i in range(1000):
        max_steps = 1000
        assign = min_conflicts(max_steps)
        if assign != -1:
            #print(assign)
            for key in assign:
                fh2.write(str(assign[key]))
                fh2.write("\n")
            break
    cons = []
    domainValues = []
    variables = []
    fh1.close()
    fh2.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("The number of arguments must be at least 2")
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    #tstart = datetime.now()
    main(input_file, output_file)
    #tend = datetime.now()
    #print("time:", (tend - tstart).microseconds / 1000)
    #print(ssteps)