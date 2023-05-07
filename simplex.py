import numpy as np


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
        pivot_row = np.argmin(ratios) + 1
        return pivot_row, pivot_col

    def __pivot__(self):
        """
        Pivot on the pivot element
        """
        pivot_row, pivot_col = self.__find_pivot__()
        pivot = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row, :] /= pivot
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
        """
        basic_vars = self.__get_basic__()
        if np.all(self.tableau[0, basic_vars] != 0):
            return 'Optimal'
        elif np.any(self.tableau[0, basic_vars] == 0):
            return 'Infinitive'
        else:
            return 'Unbounded'
    
    def solve(self):
        """
        Solve the linear program
        """
        self.tableau = self.__create_tableau__()
        while np.any(self.tableau[0, :-1] < 0):
            self.tableau = self.__pivot__()
        return self

    def get_solution(self, slack=False):
        return self.__get_solution__(slack) if self.__get_status__() != 'Unbounded' else np.inf

    def get_optimal_value(self):
        return self.__get_optimal_value__()
    
    def get_status(self):
        return self.__get_status__()
    

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
        Find pivot column and row using Bland's rule
        """
        pivot_col = np.argmin(self.tableau[0, :-1])
        if self.tableau[0, pivot_col] >= 0:
            return None, None
        ratios = np.array([self.tableau[i, -1] / self.tableau[i, pivot_col] if self.tableau[i, pivot_col] > 0 
                           else np.inf for i in range(1, self.tableau.shape[0])])
        # Apply Bland's rule to choose the pivot row in case of tie
        min_ratio_indices = np.where(ratios == ratios.min())[0]
        pivot_row = min_ratio_indices[np.argmin([np.argmin(self.tableau[min_ratio_indices + 1, :-1] > 0) 
                                                 for i in min_ratio_indices])] + 1
        return pivot_row, pivot_col

    def __pivot__(self):
        """
        Pivot on the pivot element
        """
        pivot_row, pivot_col = self.__find_pivot__()
        pivot = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row, :] /= pivot
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
        """
        basic_vars = self.__get_basic__()
        if np.all(self.tableau[0, basic_vars] != 0):
            return 'Optimal'
        elif np.any(self.tableau[0, basic_vars] == 0):
            return 'Infinite solution'
        else:
            return 'Unbounded'

    def solve(self):
        """
        Solve the linear program
        """
        self.tableau = self.__create_tableau__()
        while np.any(self.tableau[0, :-1] < 0):
            self.tableau = self.__pivot__()
        return self
    
    def get_solution(self, slack=False):
        return self.__get_solution__(slack) if self.__get_status__() == 'Optimal' else np.inf

    def get_optimal_value(self):
        return self.__get_optimal_value__()
    
    def get_status(self):
        return self.__get_status__()


class TwoPhaseSimplexSolver():
    pass   