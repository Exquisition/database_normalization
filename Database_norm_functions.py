'''
Database normalization tools

Functions include
-closure
-Minimal key (candidate key)
-projection
-Minimal basis
-Boyce Codd normal form Decomposition (BCNF)




Made by: Andy Zhou
Dec 27, 2018
'''



from itertools import *


def closure(Attributes, FDs):
    '''

    :param Attributes: set of attributes for which we want to compute the closure
    :param FDs: set of tuples where LHS -> RHS is represented by ('AB', 'CD')
    :return: the closure of the attributes in a set
    '''


    closure = set(Attributes)  #initialize closure to be just the set of attributes


    for FD in FDs:
        #for each FD in the set of FDs
        if set(FD[0]).issubset(closure):

            #such that the LHS of the FD is in the closure
            closure.add(FD[1])

            #add the RHS of the FD to the closure

    closure_string = "".join(str(s) for s in closure)
    closure_string = "".join(sorted(set(closure_string)))

    return closure_string





def FD_follows(S, FD):
    y_closure = closure(FD[0], S)
    return (FD[1] in y_closure)



def convert(Attributes):
    Attributes_string = "".join(str(s) for s in Attributes)
    Attributes_string = "".join(sorted(set(Attributes_string)))

    return Attributes_string







def findMinimalKeys(Attributes, FDs):
    '''

    :param Attributes:  attributes of the relation
    :param FDs:         set of FDs
    :return:
    '''

    key = set(Attributes)

    for A in key:
        closureK_A = closure(key.difference(A), FDs)

        if set(closureK_A) == set(convert(Attributes)):
            key = key.difference(A)

    return convert(key)



def project(Attributes, FDs):
    T = set({})
    Attributes = convert(Attributes)
    subsets = powerSet(list(Attributes))

    for subset in subsets:
        if subset:
            X_closure = closure(subset, FDs)

            for A in X_closure:
                if A in Attributes and A not in subset:    #nontrivial condition, still need to filter
                    subset = convert(subset)
                    T.add((subset, A))
                    #subset -> A is inferred FD


    #filtering redundant(weak) FDs and transitively inferred FDs
    filter1 = set({})
    for FD in T:
        #for each FD, we want to see if its redundant
        for FD2 in T:
            if FD[0] in FD2[0] and FD[1] == FD2[1] and FD != FD2:
                filter1.add(FD2)

            elif FD[1] == FD2[0]:
                inferred_FD = (FD[0], FD2[1])
                if inferred_FD in T:
                    filter1.add(inferred_FD)


    return T.difference(filter1)





def powerSet(set):
    result = [[]]
    for element in set:
        result.extend([x + [element] for x in result])

    result.sort(key=len)
    return result



def minimalBasis(FDs):

    FDs = set(FDs)

    splitRHS = FDs

    for FD in FDs.copy():
        if len(FD[1]) > 1:
            splitRHS.remove(FD)
            for att in FD[1]:
                splitRHS.add((FD[0], att))



    #step 2: Reduce LHS of split FDs

    reduced_FDs = splitRHS

    for FD_split in splitRHS.copy():

        if len(FD_split[0]) >1:
            subsets = powerSet(list(set(FD_split[0],)))
            for subset_att in subsets:
                if closure(subset_att, splitRHS) == FD_split[1]:
                    reduced_FDs.remove(FD_split)
                    reduced_FDs.add((subset_att, FD_split[1]))

    #step 3: get rid of any redundant FDs with replication or transitivity, similar to filtering done in project()

    filter1 = set({})
    for FD in reduced_FDs:
        # for each FD, we want to see if its redundant
        for FD2 in reduced_FDs:
            if FD[0] in FD2[0] and FD[1] == FD2[1] and FD != FD2:
                filter1.add(FD2)

            elif FD[1] == FD2[0]:
                inferred_FD = (FD[0], FD2[1])
                if inferred_FD in reduced_FDs:
                    filter1.add(inferred_FD)


    reduced_FDs = reduced_FDs.difference(filter1)


    return reduced_FDs






def satisfiesBCNF(FD, setFDs, R):
    #determines if an FD within setFDs satisfies the BCNF property
    if set(closure(FD[0], setFDs)) == set(convert(R)):
        return True
    return False






def BCNF_decomp(R, F):
    '''

    :param R: set of attributes
    :param F: set of functional dependencies
    :return: a valid BCNF decomposition of R as a list of sets each representing the decomposed relations
    '''

    if isDecomposed(R, F):
        return R

    for FD in F:
        if not satisfiesBCNF(FD, F, R):
            print(FD[0])

            x_closure = closure(set(FD[0]), F)
            R1 = set(x_closure)
            R2 = R.difference(R1.difference(set(FD[0])))

            FDset1 = project(R1, F)
            FDset2 = project(R2, F)

            if isDecomposed(R1, FDset1) and R1 not in BCNF_Relations:
                BCNF_Relations.append(R1)


            elif isDecomposed(R2, FDset2) and R2 not in BCNF_Relations:
                BCNF_Relations.append(R2)

            BCNF_decomp(R1, FDset1)  #recursively decompose the relations R1 and R2 after the first decomposition
            BCNF_decomp(R2, FDset2)






def isDecomposed(R, F):
    for FD in F:
        if not satisfiesBCNF(FD, F, R):
            return False
    return True



global BCNF_Relations
BCNF_Relations = []

Attributes = {'A', 'B', 'C', 'D'}
FDs = {('A', 'B'), ('BC', 'D')}

#print(findMinimalKeys(Attributes, FDs))
#print(project(('A','B','D'), FDs))
#print(minimalBasis(FDs))
BCNF_decomp(Attributes, FDs)
print(BCNF_Relations)

