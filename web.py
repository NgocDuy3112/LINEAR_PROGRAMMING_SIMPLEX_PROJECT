import streamlit as st
import numpy as np
from utils import *
from simplex import *

st.title('SIMPLEX SOLVER')

def get_user_input():
    num_variables = st.number_input('Enter number of variables', min_value=1, max_value=50, value=2)
    num_constraints = st.number_input('Enter number of constraints', min_value=1, max_value=50, value=2)
    lp_problem = LPProblem(num_variables, num_constraints)
    target_func = st.text_input('Enter objective function', value='max 3x1 + 5x2')
    lp_problem.set_objective(target_func)
    for i in range(num_constraints):
        constraint = st.text_input('Enter constraint ' + str(i + 1), value='2x1 + 3x2 <= 4')
        lp_problem.add_constraint(constraint)
    return lp_problem

def solve(problem):
    A, b, c = problem.get_problem()
    solver = None
    if np.any(b < 0):
        solver = TwoPhaseSimplexSolver(A, b, c)
    elif np.any(b == 0):
        solver = BlandSimplexSolver(A, b, c)
    else:
        solver = DantzigSimplexSolver(A, b, c)
    solver.solve()
    solution = solver.get_solution()
    status = solver.get_status()
    optimal_value = solver.get_optimal_value()
    return solution, status, optimal_value


if __name__ == "__main__":
    problem = get_user_input()
    solution, status, optimal_value = solve(problem)
    st.write('Solution: ', solution)
    st.write('Status: ', status)
    st.write('Optimal value: ', optimal_value)