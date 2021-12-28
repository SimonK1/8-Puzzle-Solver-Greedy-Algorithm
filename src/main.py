import sys
import copy
import time


class Node:
    def __init__(self, state=None, depth=None, path=None, operation=None, hValue=None, parent=None):
        self.state = state
        self.depth = depth
        self.path = path
        self.operation = operation
        self.hValue = hValue
        self.parent = parent

    # Function for checking solvability of our puzzle
    @staticmethod
    def solvable(start_state):

        inv_count = 0
        if start_state[0][1] > start_state[0][1]:
            print("yes")
        for i in range(0, xsize):
            for j in range(0, ysize):
                if start_state[i][j] > 0:
                    for k in range(i, xsize):
                        if k == i:
                            for h in range(j + 1, ysize):
                                if start_state[k][h] > 0:
                                    if start_state[i][j] > start_state[k][h]:
                                        inv_count = inv_count + 1
                        else:
                            for p in range(0, ysize):
                                if start_state[k][p] > 0:
                                    if start_state[i][j] > start_state[k][p]:
                                        inv_count = inv_count + 1
        return inv_count

    # Heuristic Function which decides which heuristic to use according to input
    @staticmethod
    def heuristic(state, goal_state):

        # Heuristic - Displaced Tiles
        if heuristic == '1':
            score = 0
            for i in range(0, xsize):
                for j in range(0, ysize):
                    if state[i][j] != 0:
                        if state[i][j] != goal_state[i][j]:
                            score += 1
            return score

        # Heuristic - Manhatten Distance
        goalx = []
        goaly = []
        for x in range(0, xsize * ysize):
            goalx.append(0)
        for y in range(0, ysize * xsize):
            goaly.append(0)
        for i in range(0, xsize):
            for j in range(0, ysize):
                goalx[int(goal_state[i][j])] = i
                goaly[int(goal_state[i][j])] = j

        if heuristic == '2':
            score = 0
            for i in range(0, xsize):
                for j in range(0, ysize):
                    num = state[i][j]
                    if num != 0:
                        score += abs(i - goalx[num]) + abs(j - goaly[num])
            return score

    @staticmethod
    def toString(tempState):
        s = ''
        for i in tempState:
            for j in i:
                s += str(j)
        return s

    def generatechildren(self, parent, visited, h, totalNodes):

        children = set()

        # finding coordinates of 0 for generating children
        xposition, yposition = None, None
        for i in range(0, xsize):
            for j in range(0, ysize):
                if parent.state[i][j] == 0:
                    xposition = i
                    yposition = j
                    break
            if xposition is not None:
                break

        # Generating child by moving down
        if xposition is not xsize - 1:
            path = copy.deepcopy(parent.path)
            path.append("UP")

            # Creating new node
            child = Node(copy.deepcopy(parent.state), parent.depth + 1, path, "UP", None, parent)
            child.state[xposition + 1][yposition], child.state[xposition][yposition] = child.state[xposition][yposition], child.state[xposition + 1][yposition]
            child.hValue = self.heuristic(child.state, goal_state)

            # Checking if child is equal to our goal
            if child.state == goal_state:
                self.vypis(totalNodes, path, child)
            if str(child.state) not in visited:
                children.add(child)

        # Generating child by moving left
        if yposition is not 0:
            path = copy.deepcopy(parent.path)
            path.append("RIGHT")

            # Creating new node
            child = Node(copy.deepcopy(parent.state), parent.depth + 1, path, "RIGHT", None, parent)
            child.state[xposition][yposition - 1], child.state[xposition][yposition] = child.state[xposition][yposition], child.state[xposition][yposition - 1]
            child.hValue = self.heuristic(child.state, goal_state)

            # Checking if child is equal to our goal
            if child.state == goal_state:
                self.vypis(totalNodes, path, child)
            if str(child.state) not in visited:
                children.add(child)

        # Generating child by moving left
        if yposition is not ysize - 1:
            path = copy.deepcopy(parent.path)
            path.append("LEFT")

            # Creating new node
            child = Node(copy.deepcopy(parent.state), parent.depth + 1, path, "LEFT", None, parent)
            child.state[xposition][yposition + 1], child.state[xposition][yposition] = child.state[xposition][yposition], child.state[xposition][yposition + 1]
            child.hValue = self.heuristic(child.state, goal_state)

            # Checking if child is equal to our goal
            if child.state == goal_state:
                self.vypis(totalNodes, path, child)
            if str(child.state) not in visited:
                children.add(child)

        # Generating child by moving down
        if xposition is not 0:
            path = copy.deepcopy(parent.path)
            path.append("DOWN")

            # Creating new node
            child = Node(copy.deepcopy(parent.state), parent.depth + 1, path, "DOWN", None, parent)
            child.state[xposition - 1][yposition], child.state[xposition][yposition] = child.state[xposition][yposition], child.state[xposition - 1][yposition]
            child.hValue = self.heuristic(child.state, goal_state)

            # Checking if child is equal to our goal
            if self.toString(child.state) == goal_state:
                self.vypis(totalNodes, path, child)
            if str(child.state) not in visited:
                children.add(child)

        totalNodes += 1

        return children, totalNodes

    # Greedy searching algorithm
    def greedy(self):

        global flag, start_time

        totalNodes = 0
        priority_queue = []
        visited = set()

        # Start of timer
        start_time = time.time()

        # Initialisation of root node
        startNode = Node(start_state, 1, [], '', self.heuristic(start_state, goal_state), None)

        # Putting root into priority queue
        priority_queue.append(startNode)

        # Infinite while
        while 1:

            # Sorting our priority queue according to heuristic value + deleting node
            priority_queue.sort(key=lambda x: x.hValue)
            currentNode = priority_queue.pop(0)

            # Adding current node into the array of visited states
            visited.add(str(currentNode.state))

            # Check if current node is equal to our final state and start writing output
            if currentNode.state == goal_state:
                self.vypis(totalNodes, currentNode.path, currentNode)

            # Generate children according to our current node
            tchilds, totalNodes = self.generatechildren(currentNode, visited,
                                                        self.heuristic(currentNode.state, goal_state), totalNodes)

            # Adding generated children to our priority queue
            for i in tchilds:
                priority_queue.append(i)

    @staticmethod
    def printFinal(totalNodes, curPath, parent):

        # Printing of solved sequence
        while 1:
            for u in range(0, xsize):
                for j in range(0, ysize):
                    print(parent.state[u][j], '', end='')
                print('\n')
            print("_________")
            if parent.parent is None:
                break
            parent = parent.parent

        # Printing additional information
        print("Moves", str(len(curPath)))
        print(curPath)
        print("Total Nodes Visited:", str(totalNodes))
        print("Time:", str(time.time() - start_time))
        sys.exit()


# Program initialisation

print("8-Puzzle solver by Greedy Algorithm")
print("___________________")
print("If you want to start testing phase type 'test' or type 'puzzle' for your own combination")
print("___________________")
test = input()

if test == 'test':
    print("Select number of test 1-12")
    ntest = input()
    if ntest == '1':
        size = '3'
        y = '7 8 6 5 4 3 2 0 1'  # Unsolvable
        x = '1 2 3 4 5 6 7 8 0'
    if ntest == '2':
        size = '3'
        y = '8 1 2 0 4 3 7 6 5'  # Unsolvable
        x = '1 2 3 4 5 6 7 8 0'
    if ntest == '3':
        size = '3'
        y = '1 8 2 0 4 3 7 6 5'  # Solvable
        x = '1 2 3 4 5 6 7 8 0'
    if ntest == '4':
        size = '3'
        y = '1 8 3 6 2 7 4 0 5'
        x = '1 2 3 8 0 4 7 6 5'
    if ntest == '5':
        size = '3'
        y = '8 0 6 5 4 7 2 3 1'
        x = '1 2 3 4 5 6 7 8 0'
    if ntest == '6':
        size = '3'
        y = '8 6 7 2 5 4 3 0 1'
        x = '1 2 3 4 5 6 7 8 0'
    if ntest == '7':
        size = '3'
        y = '6 4 7 8 5 0 3 2 1'
        x = '1 2 3 8 0 4 7 6 5'
    if ntest == '8':
        size = '3'
        y = '8 0 6 5 4 7 2 3 1'
        x = '1 2 3 8 0 4 7 6 5'
    if ntest == '9':
        size = '2'
        y = '2 1 3 4 5 6 0 7'
        x = '1 2 3 4 5 6 7 0'
    if ntest == '10':
        size = '2'
        y = '2 1 4 3 5 6 0 7'
        x = '1 2 3 4 5 6 7 0'
    if ntest == '11':
        size = '1'
        y = '1 3 2 4 0 5'
        x = '1 2 3 4 5 0'
    if ntest == '12':
        size = '1'
        y = '4 3 2 1 0 5'
        x = '1 2 3 4 5 0'
else:
    # Selecting size
    print("Select size: 3 - 3x3 or 2 - 4x2 or 1 - 3x2")
    size = input()

    # Start State
    print("Please set your start state in form 1 2 3...")
    print("Insert 0 (Zero) as blank square")
    y = input()

    # Goal State
    print("Please set your final state in form 1 2 3...")
    print("Insert 0 (Zero) as blank square")
    x = input()

print("Thank you")
print("We will solve this for you")

start = y.split()
end = x.split()

# Check if input is correct

if size == '3' and (len(start) != 9 or len(end) != 9):
    print("You entered combination that does not fit this matrix")
    sys.exit()
if size == '2' and (len(start) != 8 or len(end) != 8):
    print("You entered combination that does not fit this matrix")
    sys.exit()
if size == '1' and (len(start) != 6 or len(end) != 6):
    print("You entered combination that does not fit this matrix")
    sys.exit()

# setting sizes of X and Y according to input size
if size == '1':
    xsize = 3
    ysize = 2

if size == '2':
    xsize = 4
    ysize = 2

if size == '3':
    xsize = 3
    ysize = 3

# Transforming input into 2D array
start_state = []
for i in range(0, xsize):
    start_state.append([])
    for j in range(0, ysize):
        start_state[i].append(int(start[j + i * ysize]))

goal_state = []
for i in range(0, xsize):
    goal_state.append([])
    for j in range(0, ysize):
        goal_state[i].append(int(end[j + i * ysize]))

# Checking if puzzle is not already solved
if goal_state == start_state:
    print("There is nothing to solve, 8-Puzzle is already solved")
    sys.exit()

# Checking if puzzle is solvable + Choosing heuristic + start of searching algorithm
obj = Node()
pocet = obj.solvable(start_state)

global heuristic

if pocet % 2 == 0:
    print("It is solvable")
    print("Choose Heuristic to Use:")
    print("1 Displaced Tiles")
    print("2 Manhatten distance")
    heuristic = input()
    obj.heuristic(start_state, goal_state)
    if heuristic == '1':
        obj.greedy()
    if heuristic == '2':
        obj.greedy()
else:
    print("It is not solvable")
