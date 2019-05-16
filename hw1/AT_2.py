from collections import namedtuple

### set used to represent our NFA and DFA
Q_N = [] # Q_N
F_N = set()   # F_N

### definition of NFA state (using namedtuple)
###     num : state number
###     isFinal : whether this NFA state is in F_N or not
###     by_0 : a set of NFA state numbers (after reading input 0)
###     by_1 : a set of NFA state numbers (after reading input 1)
###     by_1 : a set of NFA state numbers (after reading input e, or without reading)
NState = namedtuple("NState", ["num", "isFinal", "by_0", "by_1", "by_e"])

### input 1
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

    state = NState(*info_list)     # get a NFA state from the field values we've gotten just before
    Q_N.append(state)              # add that state to Q_N

### get F_N
for Q in Q_N :
    if (Q.isFinal == 1) :
        F_N.add(Q.num)

### get E(q), where q is a NFA state
### return : a set of NFA state numbers
def E(state_num) :
    state = Q_N[state_num]
    result = set()
    result.add(state_num)
    for next in state.by_e :
        if (next != state_num) :
            result = result | E(next)
    return result

### get E(P), where P is a set of NFA states
### return : a set of NFA state numbers
def E_set(state_num_set) :
    result = set()
    for state_num in state_num_set :
        result = result | E(state_num)
    return result

### transiton from a set of NFA states to another set of NFA states (when reading 0)
### return : a set of NFA state numbers
def transition_by_0(state_num_set) :
    result = set()
    for state_num in state_num_set :
        result = result | Q_N[state_num].by_0
    return result

### transiton from a set of NFA states to another set of NFA states (when reading 1)
### return : a set of NFA state numbers
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

### input 2
input_list = []
M = int(input().strip())
for i in range(0, M) :
    line = input().strip()
    input_list.append(line)

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