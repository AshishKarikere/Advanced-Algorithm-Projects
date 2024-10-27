"""Preamble: This Python Program solves the 3-CNF SAT Problem and returns True if the given Formula is Satisfiable
                along with literals that have to be set to true, False if the formula is not satisfiable."""


# The below function reads the cnf file and stores the given clauses as list of lists
def read_cnf_file(file_path):
    cnf = []  # Contains all the clauses with each clause in a list
    # Opens the given cnf file and reads it, ignores the lines that start with p and only reads lines that start with c
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c'):
                continue
            elif line.startswith('p'):
                # Get the number of variables and clauses
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
            else:
                # Parse the clause
                clause = list(map(int, line.split()[:-1]))
                cnf.append(clause)
    return num_vars, num_clauses, cnf[:-2]


# Returns the negation of a literal based on the number of clauses
def negate_literal(F, l):
    # If the literal number is between 1 to max number of literals then negation would be literal number plus number
    # of literals
    if l <= F.num_vars:
        return (F.num_vars + l)
    # If the literal number is greater than max number of literals then negation would be literal number minus number
    # of literals
    return l - F.num_vars


# The Function Simplifies The given Formula F with the literal l
def Simplify(F, l):
    erased_clause = []  # Set of erased clauses after l is set to treu
    satisfied_clause = []  # The same as satisfied clause
    neg_l = negate_literal(F, l)  # Gets the negation of a literal

    # Loop for setting the value of l to tue and changing the data structures accordingly
    for Ck in F.literal_map[str(l)][1]:
        # Evaluates the Clause only if it is active that is status is grater than -1
        if F.clause_map[str(Ck)][0] > -1:
            F.clause_map[str(Ck)][0] = -1  # Sets the status to -1 and hence makes the
            erased_clause.append(Ck)  # Appends the clause to the erased list
            # Alters every literal after erasing or satisfying a clause
            for affected_lit in F.clause_map[str(Ck)][1]:
                if affected_lit != l:
                    F.literal_map[str(affected_lit)][0] = F.literal_map[str(affected_lit)][0] - 1
                    F.literal_map[str(affected_lit)][1].remove(Ck)
                    F.literal_map[str(affected_lit)][1].append(Ck)
                    if F.literal_map[str(affected_lit)][0] == 0:
                        F.pure_literal_list.append(affected_lit)
            # if elif block for re evaluating the list of 1,2, or 3 clauses
            if Ck in F.clause_list_3:
                F.clause_list_3.remove(Ck)
            elif Ck in F.clause_list_2:
                F.clause_list_2.remove(Ck)
            elif Ck in F.clause_list_1:
                F.clause_list_1.remove(Ck)
            F.clause_count = F.clause_count - 1  # Reduce the clauses count after satisfying it
            satisfied_clause.append(Ck)

        if F.clause_count == 0:
            return True

        literal_erased_clauses = []  # Contains list of erased clauses

    # Loop for evaluating the negation of literal and its after effects
    for Ck in F.literal_map[str(neg_l)][1]:
        # For evaluating the clauses where neg_l is erased from and changing the data structures accordingly
        if F.clause_map[str(Ck)][0] > 0:
            # Altering the position of the erased literal moving it to the end
            F.clause_map[str(Ck)][1].remove(neg_l)
            F.clause_map[str(Ck)][1].append(neg_l)
            # Reducing the no of literals after erasing neg_l
            F.clause_map[str(Ck)][0] = F.clause_map[str(Ck)][0] - 1
            literal_erased_clauses.append(Ck)  # Appending Ck to the list of clauses from which neg_l is removed
            # If else block that removes the Ck from one type of clause list and adds it to other clause list
            if F.clause_map[str(Ck)][0] == 0:
                return False
            elif F.clause_map[str(Ck)][0] == 1:
                F.clause_list_2.remove(Ck)
                F.clause_list_1.append(Ck)
            elif F.clause_map[str(Ck)][0] == 2:
                F.clause_list_3.remove(Ck)
                F.clause_list_2.append(Ck)

    # Appending the stack that is created from this change to the stack of the F clause
    F.stack.append([l, satisfied_clause, literal_erased_clauses])


# The function that deals with Pure literals if there are any
def PureLiteral(F):
    # While loop executes as long as there are pure literals in the list
    while (len(F.pure_literal_list)):
        l = F.pure_literal_list[0]  # Each pure literal at a time
        # Call the Simplify function with the Pure Literal
        if Simplify(F, l) == False:
            return False
        elif Simplify(F, l) == True:
            return True
        F.pure_literal_list.remove(l)  # Remove the Pure Literal from the Pure Literal List after its used in
        # Simplification


# The function is Similar to the above function but Simplifies using A Simple Literal
# From 1 literal clause
def SingleLiteralClause(F):
    while (len(F.clause_list_1)):
        Cl = F.clause_list_1.pop()
        l = F.clause_map[str(Cl)][1][0]
        if Simplify(F, l) == False:
            return False
        elif Simplify(F, l) == True:
            return True
        # F.clause_list_1.remove(Cl)
    # return Solve(F)


# Function that restores the CNF formula after backtracking
def Restore(F, stack, l):
    main_stack = []  # Picks up the stack for the given literal
    for l_stack in F.stack:
        if l_stack[0] == l:
            main_stack = l_stack
            F.stack.remove(l_stack)
            break

    satisfied_clause_list = main_stack[1]  # Satisfied clause list from the main stack
    literal_erasedclause_list = main_stack[2]  # Erased clause list from the main stack

    # Works on restoring the clauses that were satisfied when l was set to true
    for Ck in satisfied_clause_list:
        occurence = 0  # Counts the occurance
        for literal_stack in F.stack:
            for clause in literal_stack[2]:
                if clause == Ck:
                    occurence = occurence + 1

        Ck_noliterals = len(F.cnf[Ck - 1]) - occurence
        F.clause_map[str(Ck)][0] = Ck_noliterals

        # Alters the 1, 2, 3 clause list after restoration
        if Ck_noliterals == 1:
            F.clause_list_1.append(Ck)
        elif Ck_noliterals == 2:
            F.clause_list_2.append(Ck)
        elif Ck_noliterals == 3:
            F.clause_list_3.append(Ck)
    F.literal_map[str(l)][0] = len(satisfied_clause_list)

    # Following code for restoring the erased negated clause
    neg_literal_status = 0
    for Ck in literal_erasedclause_list:
        F.clause_map[str(Ck)][0] = F.clause_map[str(Ck)][0] + 1
        neg_l = negate_literal(F, l)
        F.clause_map[str(Ck)][1].remove(neg_l)
        F.clause_map[str(Ck)][1].insert(0, neg_l)
        neg_literal_status = neg_literal_status + 1
        initial_noliterals = F.clause_map[str(Ck)][0]

        # Works on the clause lists after the restoration
        if initial_noliterals == 1:
            F.clause_list_1.append(Ck)
        elif initial_noliterals == 2:
            F.clause_list_1.remove(Ck)
            F.clause_list_2.append(Ck)
        elif initial_noliterals == 3:
            F.clause_list_2.remove(Ck)
            F.clause_list_3.append(Ck)
    F.literal_map[str(neg_l)][0] = neg_literal_status


# The solve function that mainly works on the Solving the CNF Formula
def Solve(F):
    # Takes into account the Pure Literal and uses simplify with it
    if PureLiteral(F) == True:
        return True
    elif PureLiteral(F) == False:
        return False

    # Simplifies with Single Literal clause
    if SingleLiteralClause(F) == True:
        return True

    elif SingleLiteralClause(F) == False:
        return False

    # Simplifies with clauses of Length 2
    if len(F.clause_list_2) > 0:
        cl1 = F.clause_list_2[0]
        lh1 = F.clause_map[str(cl1)][0]

        # First brach with lh1 = true
        if Simplify(F, lh1) == True:
            return True
        if Simplify(F, lh1) == False:
            return False

        if Solve(F) == True:
            return True

        Restore(F, F.stack, lh1)  # Restoring the stack during backtracking if branch1 gives no good result

        # Works on Branch 2 with lh1 = False, lh2 = true
        neg_lh1 = negate_literal(F, lh1)
        if Simplify(F, neg_lh1) == True:
            return True
        if Simplify(F, neg_lh1) == False:
            return False

        lh2 = F.clause_map[str(cl1)][1]
        if Simplify(F, lh2) == True:
            return True
        if Simplify(F, lh2) == False:
            return False

        if Solve(F) == True:
            return True
        Restore(F, F.stack, lh2)
        Restore(F, F.stack, neg_lh1)  # Restore if this branch has to be backtracked
        return False

    # Works on clauses of length 3
    else:
        cl1 = F.clause_list_3[0]
        lh1 = F.clause_map[str(cl1)][0]

        # First Branch with lh1 = true
        if Simplify(F, lh1) == True:
            return True
        if Simplify(F, lh1) == False:
            return False

        if Solve(F) == True:
            return True

        Restore(F, F.stack, lh1)  # Restoation with backtracking in first branch
        neg_lh1 = negate_literal(F, lh1)
        if Simplify(F, neg_lh1) == True:
            return True
        if Simplify(F, neg_lh1) == False:
            return False

        # Works on Branch 2
        lh2 = F.clause_map[str(cl1)][1][1]
        if Simplify(F, lh2) == True:
            return True
        if Simplify(F, lh2) == False:
            return False

        if Solve(F) == True:
            return True
        Restore(F, F.stack, lh2)

        neg_lh2 = negate_literal(F, lh2)
        if Simplify(F, neg_lh2) == True:
            return True
        if Simplify(F, neg_lh2) == False:
            return False

        # Works on Branch 3
        lh3 = F.clause_map[str(cl1)][1][2]
        if Simplify(F, lh3) == True:
            return True
        if Simplify(F, lh3) == False:
            return False

        if Solve(F) == True:
            return True
        Restore(F, F.stack, lh3)
        Restore(F, F.stack, neg_lh2)
        Restore(F, F.stack, neg_lh1)
        return False

def print_satisfying_assignment(F, result):

    satisfing_literals = []
    if result == True:
        for stack in F.stack:
            satisfing_literals.append(stack[0])
        satisfing_literals = list(dict.fromkeys(satisfing_literals))
        print(" The 3-CNF Becomes true when these Literals are set to true:", satisfing_literals)

    elif result == False:
        print("There is no satisfying Assignment")

# Formula class that acts as blueprint for CNF Formula
class Formula:

    # Constructor function that displays all the variables in Formula Object
    def __init__(self, cnf, num_vars, num_clauses):
        self.cnf = cnf
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.clause_count = num_clauses
        self.clause_map = {}
        self.literal_map = []
        self.clause_list_1 = []
        self.clause_list_2 = []
        self.clause_list_3 = []
        self.pure_literal_list = []
        self.stack = []

    # Function that represents negatively numbered clauses into positive ones accordingly
    def adjust_clause_num(self):
        for i in range(len(self.cnf)):
            for j in range(len(self.cnf[i])):
                if self.cnf[i][j] < 0:
                    cl = -1 * self.cnf[i][j] + self.num_vars
                    self.cnf[i][j] = cl

    # Generates the initial Clause List from the given CNF Formula
    def generate_clause_map(self):
        for i in range(self.num_clauses):
            self.clause_map[str(i + 1)] = [len(self.cnf[i]), self.cnf[i]]

    # Generates the Literal Map from the given CNF Formula
    def generate_literal_map(self):
        for i in range(2 * num_vars):
            self.literal_map.append([])
            for j in range(len(cnf)):
                for k in range(len(cnf[j])):
                    if (i + 1) == cnf[j][k]:
                        self.literal_map[i].append(j + 1)
        literal_map2 = {}
        for i in range(len(self.literal_map)):
            literal_map2[str(i + 1)] = [len(self.literal_map[i]), self.literal_map[i]]
        self.literal_map = literal_map2

    # Generates the 1, 2 and 3 clause list initially
    def generate_clause_list(self):
        for i in range(len(cnf)):
            if len(cnf[i]) == 1:
                self.clause_list_1.append(i + 1)
            elif len(cnf[i]) == 2:
                self.clause_list_2.append(i + 1)
            elif len(cnf[i]) == 3:
                self.clause_list_3.append(i + 1)

    # Function to generate Stack initially, just a dummy function
    def generate_stack(self):
        pass

# Stores the File Path of the CNF File
file_path = 'uuf50-01.cnf'
num_vars, num_clauses, cnf = read_cnf_file(file_path)

# Creating the formula object F
F = Formula(cnf, num_vars, num_clauses)
# Printing the initial data structures
print("Initial Data Structures")
print("Number of Literals:",F.num_vars)
print("Number of cluases:", F.num_clauses)
print("Original CNF Formula:", F.cnf)

# Below functions are there to create the original Data Structures
F.adjust_clause_num()
F.generate_clause_map()
F.generate_clause_list()
F.generate_literal_map()
print("Original Clause Map:", F.clause_map)
print("Original Literal Map:", F.literal_map)
print("1 Clause List:",F.clause_list_1)
print("2 Clause List:",F.clause_list_2)
print("3 Clause List:", F.clause_list_3)
print("Stack:", F.stack)
print("Pure Literal List:", F.pure_literal_list)

# print("---------------------------------------")
l = 1
Simplify(F, l)
# print(F.clause_map)
# print(F.literal_map)
# print(F.clause_list_1)
# print(F.clause_list_2)
# print(F.clause_list_3)
# print(F.stack)
# print(F.pure_literal_list)


# print("---------------------------------------------")
Restore(F, F.stack, l)
# print(F.clause_map)
# print(F.literal_map)
# print(F.clause_list_1)
# print(F.clause_list_2)
# print(F.clause_list_3)
# print(F.stack)
# print(F.pure_literal_list)

print()
print("SOLVING THE CNF FORMULA")
result = Solve(F)
print("THe Given CNF Formula is Satisfiable: ", result)

print_satisfying_assignment(F, result)