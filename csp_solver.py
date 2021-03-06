# A CSP is modeled as a list of three elements:
# X = [X_1, X_2, ... , X_n] variables
# D = [D_1, D_2, ... , D_n] domains for each variable
# C = [C_1, C_2, ..., C_m] constraints


# Example. Map Coloring.
# Suppose we have we have the simple map drawn here:
# |------------------------------|
# |       A        |             |
# |----------------|             |
# |                |      B      |
# |       C        |             |
# |                |---|---------|
# |                |   |         |
# |----------------|   |         |
# |                    |   E     |
# |        D           |         |
# |------------------------------|



# Possible solution: {A=red, B=blue, C=green, D=orange, E=red}
# Where X = [A, B, C, D, E]
# Where D = [[red,blue,green,orange], ..., ..]
# And constraints are implicitly defined as A.color != B.color
# Explicitly: (A,B) in {(red,green), (red,blue), ... }

# Given: two variables and their shared domain as a list
# Output: a tuple containing a tuple of the variables and
# a list of constraints represented as tuples
# Example: diff_constraint('A', 'B', ['red','green']
# Output: ( ('A','B'), [('red','green'), ('green','red')] )
def diff_constraint(var1, var2, shared_domain):
    constraints = []
    for i in range(len(shared_domain)):
        for j in range(len(shared_domain)):
            if i != j:
                x = shared_domain[i]
                y = shared_domain[j]
                constraints.append((x,y))

    return ( (var1, var2), constraints )

class CSP:
    def __init__(self, Xlist, Dlist, Clist):
        # assumes that len(Xlist) == len(Dlist)
        self.domains = {}
        self.variables = Xlist
        for i in zip(Xlist, Dlist):
            var,d = i
            self.domains[var] = d
        self.constraints = {}
        for constr in Clist:
            var1,var2 = constr[0]
            lst = constr[1]
            if var1 not in self.constraints:
                self.constraints[var1] = {}
            self.constraints[var1][var2] = lst
            if var2 not in self.constraints:
                self.constraints[var2] = {}
            self.constraints[var2][var1] = lst

    def get_vars(self):
        return list(self.variables)
    def get_domains(self):
        return dict(self.domains)
    def get_constraints(self):
        return dict(self.constraints)
    

# Given a dictionary of assignments, determine if it is partial
def is_partial(assignment):
    return (None in list(assignment.values()))

def is_valid(assignment, constraints):
    if is_partial(assignment): return False
    for var in assignment:
        d = constraints[var]
        for var2 in d:
            lst = d[var2]
            a1,a2 = assignment[var],assignment[var2]
            if (a1,a2) not in lst: return False
    return True
            
# Given a CSP, returns a dictionary of a valid assignment
def solve_csp(csp):
    variables = csp.get_vars()
    domains = csp.get_domains()
    constraints = csp.get_constraints()

    assignment = {}
    for v in csp.get_vars():
        assignment[v] = None

    # dfs
    def dfs(depth):
        curr = variables[depth]
        for val in domains[curr]:
            assignment[curr] = val
            if is_valid(assignment, constraints):
                return assignment
            if 1+depth < len(variables):
                rec = dfs(1+depth)
                if rec:
                    return rec
    return dfs(0)
  



# small test example                  
# a-b-c-a in a triangle map
map_variables = ['a','b','c']
map_domains = [['red','green','blue'] for _ in range(3)]
map_constraints = []
for i in range(len(map_variables)):
    for j in range(len(map_variables)):
        if i!=j:
            v1,v2 = map_variables[i],map_variables[j]
            domain = ['red','green','blue']
            map_constraints.append(diff_constraint(v1,v2,domain))
map_csp = CSP(map_variables, map_domains, map_constraints)
map_sol = {'a': 'green', 'b': 'red', 'c': 'blue'}
# print(is_valid(map_sol, map_csp.get_constraints()))


    
map2X = ['A','B','C','D','E']
map2D = [['red','green','orange','blue'] for _ in range(5)]
map2_constr = []
map2_neighbors = {
    'A': ['B','C'],
    'B': ['A','C','D','E'],
    'C': ['A','B','D'],
    'D': ['B','C','E'],
    'E': ['B','D'] }
for v in map2X:
    for nei in map2_neighbors[v]:
        domain=['red','green','blue','orange']
        map2_constr.append(diff_constraint(v,nei,domain))

map2_csp = CSP(map2X, map2D, map2_constr)   
