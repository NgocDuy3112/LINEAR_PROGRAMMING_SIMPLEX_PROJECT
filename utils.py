import numpy as np
from simplex import *

def convert_string_to_float(string):
    try:
        if string.find('/') != -1:
            elements = string.split('/')
            return float(elements[0]) / float(elements[1])
        else:
            return float(string)
    except:
        raise Exception('Invalid number format')
    

class LPProblem():
    def __init__(self, n_variables, n_constraints, n_range_constraints):
        self.n_variables = n_variables
        self.n_constraints = n_constraints
        self.n_range_constraints = n_range_constraints
        self.variables = ['x' + str(i) for i in range(1, n_variables + 1)]
        self.constraints = []
        self.range_constraints = []
        self.neg_variables = []
        self.signed_variables = set()
        self.unsigned_variables = set()
        self.objective = None
        self.type = None
        self.A = None
        self.b = None
        self.c = None
        self.solver = None

    def __transform_objective__(self):
        elements = self.objective.split()
        problem_type = elements[0]
        c = []
        var_index = -1
        self.type = 1 if problem_type == 'min' else -1
        for i in range(2, len(elements), 2):
            var_index += 1
            if elements[i - 1][0] == '-':
                c.append(-1 * convert_string_to_float(elements[i][0])) if elements[i][0] != 'x' else c.append(-1.0)
            elif elements[i - 1][0] == '+':
                c.append(convert_string_to_float(elements[i][0])) if elements[i][0] != 'x' else c.append(1.0)
            else:
                raise Exception('Invalid objective function')
            assert elements[i][len(elements[i]) - 2:] == self.variables[var_index], 'Invalid objective function'
        self.c = np.array(c) if problem_type == 'min' else -1 * np.array(c)
        return self
    
    def __transform_constraints__(self):
        for constraint_str in self.constraints:
            elements = constraint_str.split()
            A_row = [0] * self.n_variables
            var_index = -1
            if elements[-2] == '<=':
                for i in range(1, len(elements) - 2, 2):
                    var_index = self.variables.index(elements[i][len(elements[i]) - 2:])
                    if elements[i - 1][0] == '-':
                        A_row[var_index] = (-1 * convert_string_to_float(elements[i][0])) if elements[i][0] != 'x' else -1.0
                    elif elements[i - 1][0] == '+':
                        A_row[var_index] = (convert_string_to_float(elements[i][0])) if elements[i][0] != 'x' else 1.0
                self.b = np.array([convert_string_to_float(elements[-1])]) if self.b is None else np.append(self.b, convert_string_to_float(elements[-1]))
            elif elements[-2] == '>=':
                for i in range(1, len(elements) - 2, 2):
                    var_index = self.variables.index(elements[i][len(elements[i]) - 2:])
                    if elements[i - 1][0] == '-':
                        A_row[var_index] = (convert_string_to_float(elements[i][0])) if elements[i][0] != 'x' else 1.0
                    elif elements[i - 1][0] == '+':
                        A_row[var_index] = (-1 * convert_string_to_float(elements[i][0])) if elements[i][0] != 'x' else -1.0
                self.b = np.array([-1 * convert_string_to_float(elements[-1])]) if self.b is None else np.append(self.b, -1 * convert_string_to_float(elements[-1]))
            self.A = np.array(A_row) if self.A is None else np.vstack((self.A, np.array(A_row)))
            
        return self
    
    def __transform_range_constraints__(self):
        for constraint in self.range_constraints:
            elements = constraint.split()
            if elements[1] == '<=':
                if elements[2] == '0':
                    self.signed_variables.add(elements[0])
                    idx = self.variables.index(elements[0])
                    self.A[:, idx] = -1 * self.A[:, idx]
                    self.c[idx] = -1 * self.c[idx]
                else:
                    A_row = np.zeros(self.n_variables)
                    A_row[self.variables.index(elements[0])] = 1
                    self.A = np.vstack((self.A, A_row))
                    self.b = np.append(self.b, convert_string_to_float(elements[2]))
                    self.n_constraints += 1
            elif elements[1] == '>=':
                if elements[2] == '0':
                    self.signed_variables.add(elements[0])
                if elements[2] != '0':
                    A_row = np.zeros(self.n_variables)
                    A_row[self.variables.index(elements[0])] = -1
                    self.A = np.vstack((self.A, A_row))
                    self.b = np.append(self.b, -1 * convert_string_to_float(elements[2]))
                    self.n_constraints += 1
        self.unsigned_variables = set(self.variables) - self.signed_variables
        for variable in self.unsigned_variables:
            idx = self.variables.index(variable)
            self.variables[idx] = variable + '+'
            self.variables.insert(idx + 1, variable + '-')
            self.A = np.insert(self.A, idx + 1, -1 * self.A[:, idx], axis=1)
            self.c = np.insert(self.c, idx + 1, -1 * self.c[idx])
        return self

    def __get_problem__(self):
        self.__transform_objective__()
        self.__transform_constraints__()
        self.__transform_range_constraints__()
        return self
    
    def set_objective(self, objective_str):
        self.objective = objective_str
        return self

    def add_constraint(self, constraint_str):
        if constraint_str == '':
            return self
        elements = constraint_str.split()
        if elements[-2] == '<=' or elements[-2] == '>=':
            self.constraints.append(constraint_str)
        else:
            self.constraints.append(constraint_str.replace('=', '<='))
            self.constraints.append(constraint_str.replace('=', '>='))
        return self
    
    def add_range_constraint(self, constraint_str):
        self.range_constraints.append(constraint_str)
        return self
    
    def solve(self):
        self.__get_problem__()
        if np.any(self.b < 0):
            self.solver = TwoPhaseSimplexSolver(self.A, self.b, self.c)
        elif np.any(self.b == 0):
            self.solver = BlandSimplexSolver(self.A, self.b, self.c)
        else:
            self.solver = DantzigSimplexSolver(self.A, self.b, self.c)
        self.solver.solve()
        return self
    
    def get_problem(self):
        self.__get_problem__()
        return self.A, self.b, self.c
    
    def get_solution(self):
        solution = self.solver.get_solution()
        if solution is None:
            return None
        variables = self.variables
        real_variables = set()
        for variable in variables:
            if variable[-1] == '+' or variable[-1] == '-':
                real_variables.add(variable[:-1])
            else:
                real_variables.add(variable)
        real_variables = list(real_variables)
        real_variables.sort()
        real_solution = []
        for i in range(len(variables)):
            if variables[i][-1] == '+':
                real_solution.append(solution[i] - solution[i + 1])
            elif variables[i][-1] == '-':
                continue
            else:
                real_solution.append(solution[i]) if variables[i] not in self.signed_variables else real_solution.append(-1 * solution[i])
        return dict(zip(real_variables, real_solution))

    def get_optimal_value(self):
        if self.solver.get_optimal_value() is None:
            return None
        return self.solver.get_optimal_value() * self.type
    
    def get_status(self):
        return self.solver.get_status()
    
    def __get_tableau__(self):
        return self.solver.__get_tableau__()
    
    def __get_basic__(self):
        return self.solver.__get_basic__()

    def __get_non_basic__(self):
        return self.solver.__get_non_basic__()

    
if __name__ == "__main__":
    lp_problem = LPProblem(2, 3, 2)
    lp_problem.set_objective("min - x1 + x2")
    lp_problem.add_constraint("- x1 - 2x2 <= 6")
    lp_problem.add_constraint("+ x1 - 2x2 <= 4")
    lp_problem.add_constraint("- x1 + x2 <= 1")
    lp_problem.add_range_constraint("x1 <= 0")
    lp_problem.add_range_constraint("x2 <= 0")
    
    # print(lp_problem.get_problem())
    lp_problem.solve()

    print(lp_problem.__get_tableau__())
    print(lp_problem.__get_basic__())
    print(lp_problem.__get_non_basic__())

    print(lp_problem.get_solution())
    print(lp_problem.get_optimal_value())
    print(lp_problem.get_status())