''' Test Cases '''

'''
3
S:(S)
S:SS
S:()

6
<S>:<0><2>
<S>:<S><S>
<S>:<0><1>
<0>:(
<1>:)
<2>:<S><1>
'''

'''
7
S:A2
S:1B
S:B
A:1
A:B
B:A
B:2

10
<S>:<A><0>
<S>:<1><B>
<S>:2
<S>:1
<A>:1
<A>:2
<B>:2
<B>:1
<0>:2
<1>:1
'''

'''
7
S:1
S:1B
S:AA1
S:A1
A:B
A:S
B:2

12
<S>:1
<S>:<0><B>
<S>:<A><1>
<S>:<A><0>
<B>:2
<A>:1
<A>:<0><B>
<A>:<A><1>
<A>:<A><0>
<A>:2
<0>:1
<1>:<A><0>
'''

'''
13
S:12AB
S:12B
S:12A
S:12
A:2A
A:2B
A:2
A:2AB
B:BA1
B:A1
B:B1
B:1
B:A

23
<S>:<0><2>
<S>:<0><3>
<S>:<0><4>
<S>:<0><1>
<A>:<1><A>
<A>:<1><B>
<A>:2
<A>:<1><5>
<B>:<B><6>
<B>:<A><0>
<B>:<B><0>
<B>:1
<B>:<1><A>
<B>:<1><B>
<B>:2
<B>:<1><5>
<0>:1
<1>:2
<2>:<1><5>
<3>:<1><B>
<4>:<1><A>
<5>:<A><B>
<6>:<A><0>
'''

'''
4
S:1AB
A:1A1
A:22
B:1

8
<S>:<0><2>
<A>:<0><3>
<A>:<1><1>
<B>:1
<0>:1
<1>:2
<2>:<A><B>
<3>:<A><0>
'''

'''
10
S:(X)X
S:()X
S:(X)
S:()
X:(Y
X:)Y
X:(
X:)
Y:X
Y:*

<S>:<0><2>
<S>:<0><3>
<S>:<0><4>
<S>:<0><1>
<X>:<0><Y>
<X>:<1><Y>
<X>:(
<X>:)
<Y>:*
<Y>:<0><Y>
<Y>:<1><Y>
<Y>:(
<Y>:)
<0>:(
<1>:)
<2>:<X><3>
<3>:<1><X>
<4>:<X><1>
'''

'''
8
E:E+T
E:T
T:T*F
T:F
F:(E)
F:2
F:5
F:7

22
<E>:<E><4>
<E>:<T><5>
<E>:<2><6>
<E>:2
<E>:5
<E>:7
<T>:<T><5>
<T>:<2><6>
<T>:2
<T>:5
<T>:7
<F>:<2><6>
<F>:2
<F>:5
<F>:7
<0>:+
<1>:*
<2>:(
<3>:)
<4>:<0><T>
<5>:<1><F>
<6>:<E><3>
'''


##############################################################################################################


### Check whether X is a terminal.
def isTerminal(X) :
    return ((len(X) == 1) and (not X.isalpha()))

### Check whether X is a variable.
def isVariable(X) :
    return ((len(X) == 1) and (X.isalpha()))

### Convert the form of a variable from "X" to "<X>".
def convertForm(X) :
    return "<" + X + ">"

### Find all nodes that can be reached from A in the graphs and put them onto visit.
def ConnectedNodes(A, visit):
    # Variable that is not left-side of a unit production has no neighbors.
    if (A not in P1_unit):
        return

    for N in P1_unit[A]:                # For every neighbors of A
        if (N not in visit):            # If it hasn't yet visited
            visit.add(N)                # Visit(= put it onto visit)
            ConnectedNodes(N, visit)    # Recursive call on it

### Append a data B to the entry(list) with key A in dictionary d.
def dict_append(d, A, B) :
    if (A not in d) :
        d[A] = []
    if (B not in d[A]) :
        d[A].append(B)

### Convert a string to a list like below.
### Case 1 : '1' -> ['1']
### Case 2 : '<A><B>...<Z>' -> ['<A>', '<B>', ... , '<Z>']
def list_of(str) :
    result = []

    # Case 1
    if (isTerminal(str)) :
        result.append(str)
        return result

    # Case 2
    else :
        temp_str = str[1:len(str)-1]              # remove left most and right most character
        temp_str = temp_str.replace("><", " ")  # replace "><" with a white space for splitting
        temp_list = temp_str.split()            # split by white spaces
        for e in temp_list :
            result.append("<" + e + ">")
        return result

### Debugging tool : Print all the contents of dictionary d.
def print_test(d) :
    for A in d.keys():
        print(A, d[A])
    print()


##############################################################################################################


### Construct P1.
P1 = dict()
n = int(input().strip())
Start_Var = ''
for i in range(0, n) :
    line = input().strip()
    line_split = line.split(":")
    left = line_split[0]
    right = line_split[1]
    dict_append(P1, left, right)
    if (i == 0) :
        Start_Var = left
Var = P1.keys()
'''
print("<Construct P1.>")
print_test(P1)
'''


### Construct unit productions in P1.
P1_unit = dict()
for A in Var :
    for B in P1[A] :
        if (isVariable(B)) :
            dict_append(P1_unit, A, B)
'''
print("<Construct Unit Production in P1.>")
print_test(P1_unit)
'''


##############################################################################################################


### Generating P2 (Step 2.1) : Find relations satisfying the condition "A can derive B".
P1_relation = dict()
for A in P1_unit.keys() :
    visit = set()
    ConnectedNodes(A, visit)    # Find all nodes that can be reached from A
                                # in the graphs representing unit productions in P1.
    for B in visit :
        dict_append(P1_relation, A, B)
'''
print("<Generating P2 (Step 2.1) : Find relations satisfying the condition \"A derives B\".>")
print_test(P1_relation)
'''


### Generating P2 (Step 2.2) : Add productions which are not unit to P2.
P2 = dict()
for A in Var :
    for B in P1[A] :
        if (not isVariable(B)) :
            dict_append(P2, A, B)
'''
print("<Generating P2 (Step 2.2) : In P1, choose productions which are not unit.>")
print_test(P2)
'''


### Generating P2 (Step 2.3) : Add A->x to P2, where (A can derive B) and (B->x is not unit).
for A in P1_relation.keys() :
    for B in P1_relation[A] :
        for x in P1[B] :
            if (not isVariable(x)) :
                if (not ((A in P2) and (x in P2[A]))) :
                    dict_append(P2, A, x)
Var = P2.keys()
'''
print("<Generating P2 (Step 2.3) : Add A->x to P2, when (A can derive B) and (B->x is not unit).>")
print_test(P2)
'''


##############################################################################################################


### Convert the representation of the grammar like below.
### Before : Productions of S -> ['12AB', '12B', '12A', '12]
### After  : Productions of S -> [['1', '2', '<A>', '<B>'], ['1', '2', '<B>'], ['1', '2', '<A>'], ['1', '2']]
P3 = dict()
for A in Var :
    for B in P2[A] :
        dict_append(P3, convertForm(A), list(B))
Var = P3.keys()
for A in Var :
    for B in P3[A] :
        for i, b in enumerate(B) :
            if (isVariable(b)) :
                B[i] = convertForm(b)
'''
print("<Converting the representation of the grammar.>")
print_test(P3)
'''


##############################################################################################################


### Construct a convert table for replacing a terminal with a variable.
### Map a KEY(= a terminal that should be replaced) to a VALUE(= new variable).
### KEY   : '2', '0', '1', ...
### VALUE : '<0>', '<1>', '<2>', ...
convert_table = dict()
new_var = 0
for A in Var :
    for B in P3[A] :
        if (len(B) != 1) :
            for b in B :
                if (isTerminal(b)) :
                    if (b not in convert_table) :
                        convert_table[b] = convertForm(str(new_var))
                        new_var = new_var + 1
'''
print("<Constructing a convert table for replacing a terminal with a variable.>")
for k in convert_table :
    print(k, convert_table[k])
print()
'''


### Generating P3 (Step 3.1 - 3.2) : Replace a terminal with a variable based on convert table.
for A in Var:
    for B in P3[A]:
        if (len(B) != 1):
            for i, b in enumerate(B):
                if (isTerminal(b)):
                    B[i] = convert_table[b]
for k in convert_table :
    dict_append(P3, convert_table[k], list_of(k))   # Add new variables and productions to P3.
Var = P3.keys()
'''
print("<Generating P3 (Step 3.1 - 3.2) : Replace a terminal with a variable based on convert table.>")
print_test(P3)
'''


### Generating P3 (Step 3.3) : Replace a group of variables with a variable.
### Map a KEY(= a group of variables should be replaced) to a VALUE(= new variable).
### KEY   : '<1><A><B>', '<A><0>', ...
### VALUE : '<0>', '<1>', ...
### convert_table : shared by all loop      (contians all the information aquired so far.)
### current_table : private to current loop (contains information aquired newly in current loop)
convert_table = dict()
while(True) :
    current_table = dict()
    isChanged = False

    # Construct a convert table for replacing a group of variables with a variable.
    for A in Var:
        for B in P3[A]:
            if (len(B) >= 3):
                isChanged = True
                X = "".join(B[1:])
                if (X not in convert_table) :
                    convert_table[X] = convertForm(str(new_var))
                    current_table[X] = convertForm(str(new_var))
                    new_var = new_var + 1

    if (not isChanged):
        break

    # Replace a group of variables with a variable based on convert table.
    for A in Var:
        for i, B in enumerate(P3[A]):
            if (len(B) >= 3):
                X = "".join(B[1:])
                B[1] = convert_table[X]
                P3[A][i] = B[0:2]

    # Add new variables and productions to P3.
    for k in current_table :
        dict_append(P3, current_table[k], list_of(k))
    Var = P3.keys()
'''
print("<Generating P3 (Step 3.3) : Replace a group of variables with a variable based on convert table.>")
print_test(P3)
'''


##############################################################################################################


### Output
cnt = 0
for A in Var :
    for B in P3[A] :
        cnt = cnt + 1
print(cnt)
Start_Var = convertForm(Start_Var)
for B in P3[Start_Var] :
    print(Start_Var + ":", end="")
    for e in B:
        print(e, end="")
    print()
for A in Var :
    if (A == Start_Var) :
        continue
    for B in P3[A] :
        print(A + ":", end="")
        for e in B :
            print(e, end="")
        print()
