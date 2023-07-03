import numpy as np
from scipy.optimize import linprog

class DantzigSimplexSolver():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.solution = None
        self.optimal_value = None
        self.status = None

    def solve(self):
        solver = linprog(self.c, A_ub=self.A, b_ub=self.b)
        self.solution = solver.x
        self.optimal_value = solver.fun
        self.status = solver.status
        return self
    
    def get_solution(self):
        return self.solution if self.status == 0 else None
    
    def get_optimal_value(self):
        if self.status == 0:
            return self.optimal_value
        if self.status == 3:
            return -np.inf
        return None
    
    def get_status(self):
        if self.status == 0:
            return 'Only solution'
        elif self.status == 2:
            return 'Infeasible'
        elif self.status == 3:
            return 'Unbounded'
        else:
            return 'No solution'
        

class BlandSimplexSolver():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.solution = None
        self.optimal_value = None
        self.status = None

    def solve(self):
        solver = linprog(self.c, A_ub=self.A, b_ub=self.b)
        self.solution = solver.x
        self.optimal_value = solver.fun
        self.status = solver.status
        return self
    
    def get_solution(self):
        return self.solution if self.status == 0 else None
    
    def get_optimal_value(self):
        if self.status == 0:
            return self.optimal_value
        if self.status == 3:
            return -np.inf
        return None
    
    def get_status(self):
        if self.status == 0:
            return 'Only solution'
        elif self.status == 2:
            return 'Infeasible'
        elif self.status == 3:
            return 'Unbounded'
        else:
            return 'No solution'


class TwoPhaseSimplexSolver():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.solution = None
        self.optimal_value = None
        self.status = None

    def solve(self):
        solver = linprog(self.c, A_ub=self.A, b_ub=self.b)
        self.solution = solver.x
        self.optimal_value = solver.fun
        self.status = solver.status
        return self
    
    def get_solution(self):
        return self.solution if self.status == 0 else None
    
    def get_optimal_value(self):
        if self.status == 0:
            return self.optimal_value
        if self.status == 3:
            return -np.inf
        return None
    
    def get_status(self):
        if self.status == 0:
            return 'Only solution'
        elif self.status == 2:
            return 'Infeasible'
        elif self.status == 3:
            return 'Unbounded'
        else:
            return 'No solution'