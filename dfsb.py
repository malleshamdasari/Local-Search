import copy
import sys
from collections import OrderedDict
from datetime import datetime
import time

INF = 10000000
cons = {}
variables = []
domainValues = []
domain = {}
steps = 0
pruning = 0

################################################################################
######################## Backtracking with MRV, LCV, AC-3 ######################
################################################################################

def rBackTrackSearchPlus(assignment):
    global variables
    global cons
    global domain
    global steps
    global pruning

    def isAssignmentComplete():     #check if the assignment is complete
        if len(assignment) == len(variables):
            return 0
        else:
            return -1
    def isConsistent(var, value): #check if the value is consistent
        for con in cons[var]:
            if int(con) in assignment:
                if value == assignment[int(con)]:
                    return -1
        return 0
    def getInconsistentCount(var, value): #get the inconsistent count
        count = 0
        for con in cons[var]:
            if int(con) in assignment:
                if value == assignment[int(con)]:
                    count += 1
        return count

    def removeInconsistentValues(xi, xj): #prune inconsistent values from the domain
        rm = False
        global pruning
        for x in domain[xi]:
            flag = 0
            if x in domain[xj]:
                for y in domain[xj]:
                    if x != y:
                        flag = 1
                        break
                if flag == 0:
                    l=[]
                    for c in domain[xi]:
                        if x!=c:
                            l.append(c)
                    domain.__setitem__(xi,l)
                    pruning += 1
                    rm = True
        return rm

    def ac3(var):
        queue = []
        for con in cons[var]: #append the arcs initially
            queue.append((int(con), var))
        while len(queue):
            xi, xj = queue.pop()
            if removeInconsistentValues(xi, xj):
                for xk in cons[xi]:
                    if xk != xj and int(xk) not in assignment:
                        queue.append((int(xk), xi))

    def selectUnassignedMRVVariable():
        n = INF
        mrv = []
        def remainingValues(var):
            pv = set()
            for val in domain[var]:
                for con in cons[var]:
                    if int(con) in assignment:
                        if val == assignment[int(con)]:
                            pv.add(val)
            return (len(domain[var])-len(pv))
        for var in variables:
            if var not in assignment:
                r = remainingValues(var)
                if r < n:
                    n = r
                    mrv = []
                    mrv.append(var)
                elif r == n:
                    mrv.append(var)
        return mrv[0]
    def orderLCVDomainValues(var):
        clist = {}
        for value in domain[var]:
            count = getInconsistentCount(var, value)
            if count not in clist:
                clist.__setitem__(count, [])
            clist[count].append(value)
        orderedDomainValues = OrderedDict(sorted(clist.items()))
        for val in orderedDomainValues:
            orderedDomainValues[val] = sorted(orderedDomainValues[val])
        domainValuesList = []
        for valueList in orderedDomainValues.values():
            for val in valueList:
                domainValuesList.append(val)
        return domainValuesList

    complete = isAssignmentComplete()
    if complete == 0:
        return assignment
    var = selectUnassignedMRVVariable() #Select the variable with minimum remaining values
    prevDomain = copy.deepcopy(domain) #Least constraining value should be taken
    for value in orderLCVDomainValues(var):
        consistent = isConsistent(var, value)
        if consistent == 0:
            assignment[var] = value
            domain[var] = [value]
            steps += 1
            ac3(var) #Perform AC-3
            result = rBackTrackSearchPlus(assignment)
            if result != 0:
                return result
            domain = copy.deepcopy(prevDomain)
            del assignment[var]
    return 0

###############################################################################
########################### Naive Backtrack Search ############################
###############################################################################

def rBackTrackSearch(assignment):
    global variables
    global domainValues
    global cons
    def isAssignmentComplete():
        if len(assignment) == len(variables):
            return 0
        else:
            return -1
    complete = isAssignmentComplete() #Check if the assignment is complete
    if complete == 0:
        return assignment
    def selectUnassignedVariable():
        for var in variables:
            if var not in assignment:
                return var
    def orderDomainValues(var):
        return domainValues
    def isConsistent(var, value):
        for con in cons[var]:
            if int(con) in assignment:
                if value == assignment[int(con)]:
                    return -1
        return 0

    global steps
    var = selectUnassignedVariable() # Select unassinged variable
    for value in orderDomainValues(var): #Select the ordered variable
        consistent = isConsistent(var, value) # If consistent then assign the variable with value
        if consistent == 0:
            assignment[var] = value
            steps += 1
            result = rBackTrackSearch(assignment)
            if result != 0:
                return result
            assignment.pop(var, value)
    return 0

#perform the naive or improved backtracking based on the flag.
def backTrackSearch(flag):
    if int(flag) == 0:
        return rBackTrackSearch({})
    elif int(flag) == 1:
        return rBackTrackSearchPlus({})

def main(ifile, ofile, flag):
    fh1 = open(ifile)
    fh2 = open(ofile, 'w')
    inp = []
    inp = fh1.readline().strip().split('\t')
    lines = fh1.readlines()
    global cons
    global variables
    global domainValues
    global domain
    for i in range(0,int(inp[0])):
        variables.append(i)
    for i in range(0,int(inp[2])):
        domainValues.append(i)
    for var in variables:
        domain.__setitem__(var, domainValues)
    for variable in range(int(inp[0])):
        cons.__setitem__(variable, [])
    for line in lines:
        line = line.strip().split('\t')
        if line[1] not in cons[int(line[0])]:
            cons[int(line[0])].append(line[1])
        if line[0] not in cons[int(line[1])]:
            cons[int(line[1])].append(line[0])
    #tstart = time.time()
    assign = backTrackSearch(flag)  # Call the backtracking the function
    #tend = time.time()
    #print (steps)
    #print (pruning)
    #print ("time:",(tend - tstart))
    #print (assign)
    for key in assign:
        fh2.write(str(assign[key]))
        fh2.write("\n")
    cons = []
    domainValues = []
    variables = []
    domain = []
    fh1.close()
    fh2.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("The number of arguments must be at least 3")
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mode_flag = sys.argv[3]
    main(input_file, output_file, int(mode_flag))