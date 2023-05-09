import streamlit as st
import numpy as np
from utils import *
from simplex import *

st.title('SIMPLEX SOLVER')

def get_user_input():
    num_variables = st.number_input('Enter number of variables', min_value=1, max_value=50, value=2)
    num_constraints = st.number_input('Enter number of constraints', min_value=1, max_value=50, value=2)
    num_ranges = st.number_input('Enter number of ranges', min_value=0, max_value=50, value=num_variables)
    lp_problem = LPProblem(num_variables, num_constraints)
    target_func = st.text_input('Enter objective function', value='max + 3x1 + 5x2')
    lp_problem.set_objective(target_func)
    for i in range(num_ranges):
        range_constraint = st.text_input('Enter range constraint ' + str(i + 1), value='x1 >= 0')
        lp_problem.add_range_constraint(range_constraint)
    for i in range(num_constraints):
        constraint = st.text_input('Enter constraint ' + str(i + 1), value='+ 2x1 + 3x2 <= 4')
        lp_problem.add_constraint(constraint)
    return lp_problem


def solve(problem):
    return problem.solve()


if __name__ == "__main__":
    problem = get_user_input()
    solution, status, optimal_value = solve(problem)
    if status == 'Infeasible':
        st.write('Problem is infeasible')
    elif status == 'Unbounded':
        st.write('Problem is unbounded')
    elif status == 'Infinite solution':
        st.write('Problem has infinite solutions')
        st.write('Optimal value: ', optimal_value)
    else:
        st.write('Solution: ', solution)
        st.write('Status: ', status)
        st.write('Optimal value: ', optimal_value)