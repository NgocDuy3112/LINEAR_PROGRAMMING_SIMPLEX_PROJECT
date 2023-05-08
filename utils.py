import numpy as np

class LPProblem():
    def __init__(self, n_variables, n_constraints, n_range_constraints):
        self.n_variables = n_variables
        self.n_constraints = n_constraints
        self.n_range_constraints = n_range_constraints
        self.variables = ['x' + str(i) for i in range(1, n_variables + 1)]
        self.constraints = []
        self.range_constraints = []
        self.neg_variables = []
        self.objective = None
        self.A = None
        self.b = None
        self.c = None
    
    def set_objective(self, objective_str):
        self.objective = objective_str
        return self

    def __transform_objective__(self):
        elements = self.objective.split()
        problem_type = elements[0]
        c = []
        var_index = -1
        assert problem_type == 'max' or problem_type == 'min', 'Invalid objective function'
        for i in range(2, len(elements), 2):
            var_index += 1
            if elements[i - 1][0] == '-':
                c.append(-1 * float(elements[i][0])) if elements[i][0] != 'x' else c.append(-1.0)
            elif elements[i - 1][0] == '+':
                c.append(float(elements[i][0])) if elements[i][0] != 'x' else c.append(1.0)
            else:
                raise Exception('Invalid objective function')
            assert elements[i][len(elements[i]) - 2:] == self.variables[var_index], 'Invalid objective function'
        self.c = np.array(c) if problem_type == 'min' else -1 * np.array(c)
        return self

    def add_constraint(self, constraint_str):
        elements = constraint_str.split()
        assert elements[-2] == '<=' or elements[-2] == '>=' or elements[-2] == '=', 'Invalid constraint'
        if elements[-2] == '<=' or elements[-2] == '>=':
            self.constraints.append(constraint_str)
        else:
            self.constraints.append(constraint_str.replace('=', '<='))
            self.constraints.append(constraint_str.replace('=', '>='))
        return self
    
    def add_range_constraint(self, constraint_str):
        self.range_constraints.append(constraint_str)
        return self
    
    def __transform_constraints__(self):
        for constraint_str in self.constraints:
            elements = constraint_str.split()
            A_row = []
            var_index = -1
            if elements[-2] == '<=':
                for i in range(1, len(elements) - 2, 2):
                    var_index += 1
                    if elements[i - 1][0] == '-':
                        A_row.append(-1 * float(elements[i][0])) if elements[i][0] != 'x' else A_row.append(-1.0)
                    elif elements[i - 1][0] == '+':
                        A_row.append(float(elements[i][0])) if elements[i][0] != 'x' else A_row.append(1.0)
                    else:
                        raise Exception('Invalid constraint')
                    assert elements[i][len(elements[i]) - 2:] == self.variables[var_index], 'Invalid constraint'
                self.b = np.array([float(elements[-1])]) if self.b is None else np.append(self.b, float(elements[-1]))
            elif elements[-2] == '>=':
                for i in range(1, len(elements) - 2, 2):
                    var_index += 1
                    if elements[i - 1][0] == '-':
                        A_row.append(float(elements[i][0])) if elements[i][0] != 'x' else A_row.append(1.0)
                    elif elements[i - 1][0] == '+':
                        A_row.append(-1 * float(elements[i][0])) if elements[i][0] != 'x' else A_row.append(-1.0)
                    else:
                        raise Exception('Invalid constraint')
                    assert elements[i][len(elements[i]) - 2:] == self.variables[var_index], 'Invalid constraint'
                self.b = np.array([-1 * float(elements[-1])]) if self.b is None else np.append(self.b, -1 * float(elements[-1]))
            self.A = np.array(A_row) if self.A is None else np.vstack((self.A, np.array(A_row)))
        return self
    
    
    def __transform_range_constraints__(self):
        signed_variables = set()
        for constraint in self.range_constraints:
            elements = constraint.split()
            signed_variables.add(elements[0])
            if elements[1] == '<=':
                if elements[2] == '0':
                    idx = self.variables.index(elements[0])
                    self.A[:, idx] = -1 * self.A[:, idx]
                else:
                    A_row = np.zeros(self.n_variables)
                    A_row[self.variables.index(elements[0])] = 1
                    self.A = np.vstack((self.A, A_row))
                    self.b = np.append(self.b, float(elements[2]))
                    self.n_constraints += 1
            elif elements[1] == '>=':
                if elements[2] == '0':
                    A_row = np.zeros(self.n_variables)
                    A_row[self.variables.index(elements[0])] = -1
                    self.A = np.vstack((self.A, A_row))
                    self.b = np.append(self.b, -1 * float(elements[2]))
                    self.n_constraints += 1
        unsigned_variables = set(self.variables) - signed_variables
        for variable in unsigned_variables:
            pass
        return self


    def get_problem(self):
        self.__transform_constraints__()
        self.__transform_range_constraints__()
        self.__transform_objective__()
        return self.A, self.b, self.c
    



    
if __name__ == "__main__":
    lp_problem = LPProblem(3, 3, 2)
    lp_problem.set_objective('max + 2x1 + 3x2 + 5x3')
    lp_problem.add_constraint('+ 2x1 + 3x2 + 0x3 >= 10')
    lp_problem.add_constraint('+ x1 + x2 + x3 <= 5')
    lp_problem.add_constraint('+ 2x1 + 5x2 + 5x3 = 15')
    lp_problem.add_range_constraint('+ x1 <= 0')
    # lp_problem.add_range_constraint('+ x2 <= -2')
    print(lp_problem.get_problem())