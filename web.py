import streamlit as st
from utils import *
from simplex import *

st.title('SIMPLEX SOLVER')

def get_user_input():
    num_variables = st.number_input('Enter number of variables', min_value=1, max_value=50, value=1)
    num_constraints = st.number_input('Enter number of constraints', min_value=1, max_value=50, value=1)
    num_ranges = st.number_input('Enter number of ranges', min_value=0, max_value=50, value=0)
    lp_problem = LPProblem(num_variables, num_constraints, num_ranges)
    target_func = st.text_input('Enter objective function')
    lp_problem.set_objective(target_func)
    for i in range(num_constraints):
        constraint = st.text_input('Enter constraint ' + str(i + 1))
        lp_problem.add_constraint(constraint)
    for i in range(num_ranges):
        range_constraint = st.text_input('Enter range constraint ' + str(i + 1))
        lp_problem.add_range_constraint(range_constraint)
    return lp_problem

def solve(problem):
    problem.solve()
    return problem.get_solution(), problem.get_optimal_value(), problem.get_status()

def print_solution(solution, optimal_value, status):
    st.write('Solution: ')
    for variable, value in solution.items():
        st.write(variable, '= ', value)
    st.write('Optimal value: ', optimal_value)
    st.write('Status: ', status)


if __name__ == "__main__":
    problem = get_user_input()
    if st.button("Solve"):
        solution, optimal_value, status = solve(problem)
        print_solution(solution, optimal_value, status)