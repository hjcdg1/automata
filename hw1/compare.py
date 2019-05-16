from collections import namedtuple

### set used to represent our NFA and DFA
Q_N = []
Q_D = []
F_N = set()

### definition of NFA state (using namedtuple)
###     num : state number
###     isFinal : whether this NFA state is in F_N or not
###     by_0 : a set of NFA state numbers (after reading input 0)
###     by_1 : a set of NFA state numbers (after reading input 1)
###     by_1 : a set of NFA state numbers (after reading input e, or without reading)
NState = namedtuple("NState", ["num", "isFinal", "by_0", "by_1", "by_e"])

### definition of DFA state (defining a class)
###     id : unique number to identify each DFA state
###     subset : a set of NFA state numbers, which is used to represent this DFA state
###     isFinal : whether this DFA state is in F_D or not
###     by_0 : id of a DFA state to be reached when reading input 0
###     by_1 : id of a DFA state to be reached when reading input 1
###     isMarked : whether this DFA state is marked or not
class DState :
    def __init__(self):
        self.id = 0
        self.subset = set()
        self.isFinal = 0
        self.by_0 = 0
        self.by_1 = 0
        self.isMarked = False

    def set_id(self, id):
        self.id = id
    def set_subset(self, subset):
        self.subset = subset
    def set_isFinal(self, isFinal):
        self.isFinal = isFinal
    def set_by_0(self, by_0):
        self.by_0 = by_0
    def set_by_1(self, by_1):
        self.by_1 = by_1
    def set_isMarked(self, isMarked):
        self.isMarked = isMarked

    ### get an unique number from "subset" of this state and set "id" to this value
    def set_id_from_subset(self):
        result = 0
        for state_num in self.subset:
            result = result + pow(2, state_num)
        self.id = result

### input
N = int(input().strip())
for i in range(0, N) :
    line = input().strip()
    info_list = line.split()
    info_list[0] = int(info_list[0].strip())    # get "num" field value
    info_list[1] = int(info_list[1].strip())    # get "isFinal" field value

    set_0 = set()
    if (info_list[2].strip() != "-") :
        by_0_list = info_list[2].strip().split(",")
        for i in by_0_list:
            set_0.add(int(i))

    set_1 = set()
    if (info_list[3].strip() != "-") :
        by_1_list = info_list[3].strip().split(",")
        for i in by_1_list:
            set_1.add(int(i))

    set_e = set()
    if (info_list[4].strip() != "-"):
        by_e_list = info_list[4].strip().split(",")
        for i in by_e_list:
            set_e.add(int(i))

    info_list[2] = set_0    # get "by_0" field value
    info_list[3] = set_1    # get "by_1" field value
    info_list[4] = set_e    # get "by_e" field value

    state = NState(*info_list)     # make a NFA state from the field values we've gotten just before
    Q_N.append(state)              # add that state to Q_N

### construct F_N
for Q in Q_N :
    if (Q.isFinal == 1) :
        F_N.add(Q.num)

### get E(q), where q is a NFA state
### (a NFA state number) -> (a set of NFA state numbers)
def E(state_num) :
    state = Q_N[state_num]
    result = set()
    result.add(state_num)
    for next in state.by_e :
        if (next != state_num) :
            result = result | E(next)
    return result

### get E(P), where P is a set of NFA states
### (a set of NFA state numbers) -> (a set of NFA state numbers)
def E_set(state_num_set) :
    result = set()
    for state_num in state_num_set :
        result = result | E(state_num)
    return result

### transiton from a set of NFA states to another set of NFA states (when reading 0)
### (a set of NFA state numbers) -> (a set of NFA state numbers)
def transition_by_0(state_num_set) :
    result = set()
    for state_num in state_num_set :
        result = result | Q_N[state_num].by_0
    return result

### transiton from a set of NFA states to another set of NFA states (when reading 1)
### (a set of NFA state numbers) -> (a set of NFA state numbers)
def transition_by_1(state_num_set) :
    result = set()
    for state_num in state_num_set :
        result = result | Q_N[state_num].by_1
    return result

### determine whether given set of states contains a state in F_N
def set_containsFinal(state_num_set) :
    for state_num in state_num_set :
        if (state_num in F_N) :
            return True
    return False


### Initialization Step (Algorithm : 21 page in our textbook)
DFA_set = set()     # An id in this set indicates that the corresponding DFA state is in Q_D.
initial_state = DState()
initial_state.set_subset(E(0))
initial_state.set_id_from_subset()
initial_state.set_isMarked(True)
Q_D.append(initial_state)
DFA_set.add(initial_state.id)

### Iteration (Algorithm : 21-22 pages in our textbook)
isFound = False
while (True) :
    isFound = False
    for Q in Q_D :
        if (Q.isMarked) :   # a marked state P in Q_D is found
            isFound = True
            Q.set_isMarked(False)   # unmark Q

            # for input 0
            R = DState()
            R.set_subset(E_set(transition_by_0(Q.subset)))
            R.set_id_from_subset()

            if R.id not in DFA_set :    # If R is not in Q_D, add R as marked state to Q_D
                R.set_isMarked(True)
                Q_D.append(R)
                DFA_set.add(R.id)
            Q.set_by_0(R.id)            # Q --(0)--> R

            # for input 1
            R = DState()
            R.set_subset(E_set(transition_by_1(Q.subset)))
            R.set_id_from_subset()
            if R.id not in DFA_set:     # If R is not in Q_D, add R as marked state to Q_D
                R.set_isMarked(True)
                Q_D.append(R)
                DFA_set.add(R.id)
            Q.set_by_1(R.id)            # Q --(1)--> R

            break

    if (isFound == False) :
        break

### replace each value of id with actual DFA state number (by constructng a table)
table = dict()
for i, Q in enumerate(Q_D) :
    table[Q.id] = i
for i, Q in enumerate(Q_D) :
     Q.set_id(table[Q.id])
     Q.set_by_0(table[Q.by_0])
     Q.set_by_1(table[Q.by_1])

### determine which DFA state is in F_D
for Q in Q_D :
    flag = False
    for q in Q.subset :
        if (q in F_N) :
            flag = True
            break
    if (flag) :
        Q.set_isFinal(1)
    else :
        Q.set_isFinal(0)

### input 2
input_list = []
M = int(input().strip())
for i in range(0, M) :
    line = input().strip()
    input_list.append(line)

### transition function of our DFA
def next_state(state, c) :
    if (c == "0") :
        return state.by_0
    elif (c == "1") :
        return state.by_1

### for each input string, print "Yes" if accept, "No" otherwise
print("*** Output of DFA ***")
for str in input_list :
    current = Q_D[0]
    for c in str :
        current = Q_D[next_state(current, c)]
    if (current.isFinal == 1) :
        print("Yes")
    else :
        print("No")

print()

print("*** Output of NFA ***")
for str in input_list :
    current = E(0)
    for c in str :
        if (c == "0") :
            temp = transition_by_0(current)
        elif (c == "1") :
            temp = transition_by_1(current)
        current = E_set(temp)
    if (set_containsFinal(current)) :
        print("Yes")
    else :
        print("No")