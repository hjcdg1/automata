''' Test Cases '''

'''
8
S:AB
S:BC
A:BA
A:1
B:CC
B:2
C:AB
C:1
21121

Yes
'''

'''
6
S:XZ
S:SS
S:XY
X:(
Y:)
Z:SY
((()))()

Yes
'''


##############################################################################################################


### Append a data B to the entry(list) with key A in dictionary d.
def dict_append(d, A, B) :
    if (A not in d) :
        d[A] = []
    if (B not in d[A]) :
        d[A].append(B)

### Check whether X is a terminal.
def isTerminal(X) :
    return ((len(X) == 1) and (not X.isalpha()))

### Debugging tool : Print all the contents of dictionary d.
def print_test(d) :
    for A in d.keys():
        print(A, d[A])
    print()

### Debugging tool : Print V[i][j] for all i and j.
def print_V(V) :
    for i in range(0, n) :
        for j in range(0, n) :
            print(V[i][j], end=" ")
        print()


##############################################################################################################


### Construct P1.
P = dict()
S = ''
N = int(input().strip())
for i in range(0, N) :
    line = input().strip()
    line_split = line.split(":")
    left = line_split[0]
    right = line_split[1]
    dict_append(P, left, right)
    if (i == 0) :
      S = left
Var = P.keys()
w = input()
n = len(w)


### Single : Productions of the form A->a
### Double : Productions of the form A->BC
Single = dict()
Double = dict()
for A in Var :
    for B in P[A] :
        if (isTerminal(B)) :
            dict_append(Single, A, B)
        else :
            dict_append(Double, A, B)


### Initialzie V
V = []
for i in range(0, n) :
    temp = []
    for j in range(0, n) :
        temp.append(set())
    V.append(temp)


##############################################################################################################


### CYK Algorithm (based on pseudo-code in text book)
for i in range(0, n):
    for A in Single.keys():
        for a in Single[A]:
            if (a == w[i]):
                V[i][i].add(A)
for d in range(1, n):
    for i in range(0, n - d):
        j = i + d
        for k in range(i, j):
            for A in Double.keys():
                for BC in Double[A]:
                    if ((BC[0] in V[i][k]) and (BC[1] in V[k + 1][j])):
                        V[i][j].add(A)

print_V(V)
##############################################################################################################


### Output
if (S in V[0][n-1]) :
    print("Yes")
else :
    print("No")
