''' test case '''

''' add(x, y)
0
5
00001
- - -
- - -
1 # R
1 1 R
1 1 R
2 # L
- - -
3 # L
- - -
- - -
3 1 L
4 # S
- - -
- - -
- - -
'''

''' (0^n)(1^n)
2
6
000001
1 a R
- - -
0 # R
- - -
3 b R
1 0 R
2 b L
- - -
- - -
1 b R
2 0 L
- - -
- - -
0 a R
2 b L
- - -
- - -
5 # S
- - -
3 b R
- - -
- - -
- - -
- - -
- - -
- - -
- - -
- - -
- - -
- - -
00001111
'''

''' max(x-y, 0)
0
8
00000001
- - -
- - -
1 # R
1 0 R
1 1 R
2 # L
5 # L
3 # L
- - -
3 0 L
3 1 L
4 # R
6 # R
1 # R
- - -
- - -
5 1 L
7 # S
- - -
6 # R
7 # S
- - -
- - -
- - -
'''

''' multiply(x, y)
2
16
0000000000000001
1 0 R
3 1 R
0 # R
- - -
- - -
- - -
1 1 R
2 # L
- - -
- - -
15 # L
2 # L
- - -
- - -
- - -
4 0 L
3 1 R
- - -
- - -
- - -
- - -
5 0 L
- - -
- - -
- - -
- - -
10 a R
6 # R
- - -
- - -
6 0 R
6 1 R
7 # L
- - -
- - -
8 1 R
7 1 L
15 # S
- - -
- - -
- - -
8 1 R
9 # L
- - -
- - -
- - -
7 # L
- - -
- - -
- - -
10 0 R
10 1 R
12 0 L
- - -
- - -
11 0 L
11 1 L
- - -
5 0 L
- - -
11 0 L
13 b R
- - -
- - -
- - -
13 0 R
13 1 R 
14 1 L
- - -
- - -
14 0 L
14 1 L
- - -
- - -
12 1 L
- - -
- - -
- - -
- - -
- - -
'''

''' [sqrt(n)]
2
15
000000000000001
- - -
- - -
1 # R
- - -
- - -
- - -
1 1 R
2 0 R
- - -
- - -
- - -
- - -
3 b L
- - -
- - -
3 0 L
3 1 L
4 # S
- - -
- - -
- - -
- - -
5 # R
- - -
- - -
5 0 R
5 1 R
- - -
- - -
6 a L
6 0 L
7 0 S
13 # R
- - -
- - -
7 0 R
- - -
12 b L
7 a R
8 a L
8 0 L
9 0 L
13 # R
8 a L
- - -
- - -
7 0 S
13 # R
- - -
- - -
- - -
- - -
11 # L
10 1 R
10 1 R
11 # L
11 1 L
14 # S
- - -
- - -
12 0 L
12 1 L
4 # S
12 b L
- - -
13 0 R
- - -
- - -
10 0 R
10 0 R
- - -
- - -
- - -
- - -
- - -
'''

# Convert a character on tape to an index into a corresponding block
def char_to_idx(c) :
    if (c == '0') :
        return 0
    elif (c == '1') :
        return 1
    elif (c == '#') :
        return 2
    else :
        return 3 + (ord(c) - ord('a'))

# Determine whether the transition is defined
def isDefined(transition) :
    if ("".join(transition) == "---") :
        return False
    else :
        return True

# Input K, N
K = int(input())
N = int(input())

# Input halt states
Halt = set()
temp = list(input())
for i in range(0, N) :
    if (int(temp[i]) == 1) :
        Halt.add(i)

# Construct transition table
transition_table = []
for i in range(0, N) :
    transition_table_block = []
    transition_table_block.append(input().split())      # transition by 0
    transition_table_block.append(input().split())      # transition by 1
    transition_table_block.append(input().split())      # transition by e
    for j in range(0, K) :                              # transition by a, b, c, . . .
        transition_table_block.append(input().split())
    transition_table.append(transition_table_block)

# Construct input tape
tape = list(input())    # current input tape (= a list of characters)
tape.insert(0, '#')     # insert a space character into the front of the tape
state = 0               # current state number
head = 0                # current head position

# repeat unitl current state becomes halting state
while (state not in Halt) :
    # Implement the fact that there exist an infinite number of white spaces at the end of the tape
    if (head >= len(tape)) :
        tape.append('#')

    block = transition_table[state]                 # transition block corresponding to the current state
    transition = block[char_to_idx(tape[head])]     # transition corresponding to the current state and tape character

    # FOR DEBUGGING : print("tape:", tape, "head:", head, "state:", state)

    # If the transition is defined
    if (isDefined(transition)) :
        state = int(transition[0])      # Change the state
        tape[head] = transition[1]      # Replace the tape character
        # Move the head
        if (transition[2] == 'R') :
            head = head + 1
        elif (transition[2] == 'L') :
            head = head - 1

    # Otherwise (Infinite loop state)
    else :
        print("Enter infinite loop")
        break

# Output
print("".join(tape))