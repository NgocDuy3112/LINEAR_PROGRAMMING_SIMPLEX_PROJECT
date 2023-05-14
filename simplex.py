import numpy as np
from scipy.optimize import linprog

class DantzigSimplexSolver():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.tableau = np.zeros((self.A.shape[0] + 1, self.A.shape[1] + self.A.shape[0] + 1))
    
    def __create_tableau__(self):
        """
        Create the tableau for the simplex method
        """
        m, n = self.A.shape
        self.tableau[0, :n] = self.c
        self.tableau[0, n:] = 0
        self.tableau[1:, :n] = self.A
        self.tableau[1:, n:-1] = np.eye(m)
        self.tableau[1:, -1] = self.b
        return self.tableau
    
    def __find_pivot__(self):
        """
        Find pivot column and row
        """
        pivot_col = np.argmin(self.tableau[0, :-1])
        if self.tableau[0, pivot_col] >= 0:
            return None, None
        ratios = np.array([self.tableau[i, -1] / self.tableau[i, pivot_col] if self.tableau[i, pivot_col] > 0 
                           else np.inf for i in range(1, self.tableau.shape[0])])
        if np.all(ratios == np.inf):
            return None, None
        pivot_row = np.argmin(ratios) + 1
        return pivot_row, pivot_col

    def __pivot__(self):
        """
        Pivot on the pivot element
        """
        pivot_row, pivot_col = self.__find_pivot__()
        pivot = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row, :] = self.tableau[pivot_row, :] / pivot
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                self.tableau[i, :] -=  self.tableau[pivot_row, :] * self.tableau[i, pivot_col]
        return self.tableau
    
    def __get_basic__(self):
        """
        Get basic variables
        """
        basics = []
        for j in range(self.tableau.shape[1] - 1):
            if np.sum(self.tableau[:, j] == 1) == 1 and np.sum(self.tableau[:, j] == 0) == (self.tableau.shape[0] - 1):
                basics.append(j)
        return basics

    def __get_non_basic__(self):
        """
        Get non-basic variables
        """
        return [i for i in range(self.tableau.shape[1] - 1) if i not in self.__get_basic__()]
    
    def __get_tableau__(self):
        """
        Get tableau
        """
        return self.tableau
    
    def __get_solution__(self, slack=False):
        """
        Get solution
        """
        solution = np.zeros(self.tableau.shape[1] - 1)
        for j in self.__get_basic__():
            row = np.where(self.tableau[:, j] == 1)[0][0]
            solution[j] = self.tableau[row, -1]
        return np.array(solution[:self.A.shape[1]]) if not slack else np.array(solution)          
    
    def __get_optimal_value__(self):
        """
        Get optimal value
        """
        return -self.tableau[0, -1]
    
    def __get_status__(self):
        """
        Get status
        - Only solution: 1
        - Unbounded: 2
        - Infinite solution: 3
        """
        non_basic_vars = self.__get_non_basic__()
        if np.all(self.tableau[0, non_basic_vars] < 0) and np.all(self.tableau[1:, non_basic_vars] >= 0):
            return 2
        elif np.any(self.tableau[0, non_basic_vars] == 0):
            return 3
        return 1
    
    def solve(self):
        """
        Solve the linear program
        """
        self.tableau = self.__create_tableau__()
        while np.any(self.tableau[0, :-1] < 0):   
            self.tableau = self.__pivot__()
            # Break condition
            if self.__get_status__() == 2:
                break
        return self

    def get_solution(self, slack=False):
        return self.__get_solution__(slack) if self.__get_status__() == 1 or self.__get_status__() == 2 else None

    def get_optimal_value(self):
        return self.__get_optimal_value__() if self.__get_status__() != 2 else None
    
    def get_status(self):
        if self.__get_status__() == 1:
            return 'Only solution'
        elif self.__get_status__() == 2:
            return 'Unbounded'
        else:
            return 'Infinite solution'

class BlandSimplexSolver():
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.tableau = np.zeros((self.A.shape[0] + 1, self.A.shape[1] + self.A.shape[0] + 1))
    
    def __create_tableau__(self):
        """
        Create the tableau for the simplex method
        """
        m, n = self.A.shape
        self.tableau[0, :n] = self.c
        self.tableau[0, n:] = 0
        self.tableau[1:, :n] = self.A
        self.tableau[1:, n:-1] = np.eye(m)
        self.tableau[1:, -1] = self.b
        return self.tableau
    
    def __find_pivot__(self):
        """
        Find pivot column and row
        """
        neg_cols = np.where(self.tableau[0, :-1] < 0)[0]
        if len(neg_cols) == 0:
            return None, None
        pivot_col = neg_cols[0]
        ratios = np.array([self.tableau[i, -1] / self.tableau[i, pivot_col] if self.tableau[i, pivot_col] > 0 
                           else np.inf for i in range(1, self.tableau.shape[0])])
        if np.all(ratios == np.inf):
            return None, None
        pivot_row = np.argmin(ratios) + 1
        return pivot_row, pivot_col

    def __pivot__(self):
        """
        Pivot on the pivot element
        """
        pivot_row, pivot_col = self.__find_pivot__()
        pivot = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row, :] = self.tableau[pivot_row, :] / pivot
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                self.tableau[i, :] -= self.tableau[i, pivot_col] * self.tableau[pivot_row, :]
        return self.tableau
    
    def __get_basic__(self):
        """
        Get basic variables
        """
        basics = []
        for j in range(self.tableau.shape[1] - 1):
            if np.sum(self.tableau[:, j] == 1) == 1 and np.sum(self.tableau[:, j] == 0) == (self.tableau.shape[0] - 1):
                basics.append(j)
        return basics

    def __get_non_basic__(self):
        """
        Get non-basic variables
        """
        return [i for i in range(self.tableau.shape[1] - 1) if i not in self.__get_basic__()]
    
    def __get_tableau__(self):
        """
        Get tableau
        """
        return self.tableau
    
    def __get_solution__(self, slack=False):
        """
        Get solution
        """
        solution = np.zeros(self.tableau.shape[1] - 1)
        for j in self.__get_basic__():
            row = np.where(self.tableau[:, j] == 1)[0][0]
            solution[j] = self.tableau[row, -1]
        return np.array(solution[:self.A.shape[1]]) if not slack else np.array(solution)          
    
    def __get_optimal_value__(self):
        """
        Get optimal value
        """
        return -self.tableau[0, -1]
    
    def __get_status__(self):
        """
        Get status
        - Only solution: 1
        - Unbounded: 2
        - Infinite solution: 3
        """
        non_basic_vars = self.__get_non_basic__()
        if np.all(self.tableau[0, non_basic_vars] < 0) and np.all(self.tableau[1:, non_basic_vars] >= 0):
            return 2
        elif np.any(self.tableau[0, non_basic_vars] == 0):
            return 3
        return 1
    
    def solve(self):
        """
        Solve the linear program
        """
        self.tableau = self.__create_tableau__()
        while np.any(self.tableau[0, :-1] < 0):
            self.tableau = self.__pivot__()
            # Break condition
            if self.__get_status__() == 2:
                break
        return self

    def get_solution(self, slack=False):
        return self.__get_solution__(slack) if self.__get_status__() == 1 or self.__get_status__() == 2 else None

    def get_optimal_value(self):
        return self.__get_optimal_value__() if self.__get_status__() != 2 else None
    
    def get_status(self):
        if self.__get_status__() == 1:
            return 'Only solution'
        elif self.__get_status__() == 2:
            return 'Unbounded'
        else:
            return 'Infinite solution'


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