import streamlit as st
from PIL import Image
from utils import *
from simplex import *

img = Image.open("images/calculator_icon.png")
st.set_page_config(page_title="Linear Programming Solver", page_icon=img)

def get_user_input():
    st.header('Define the problem')

    col1, col2, col3 = st.columns(3)
    with col1:
        num_variables = st.number_input('Enter number of variables', min_value=1, max_value=50, value=1)
    with col2:
        num_constraints = st.number_input('Enter number of constraints', min_value=0, max_value=50, value=0)
    with col3:
        num_ranges = st.number_input('Enter number of ranges', min_value=0, max_value=50, value=0)
    lp_problem = LPProblem(num_variables, num_constraints, num_ranges)

    st.divider()
    st.header('Define the objective function')
    target_func = st.text_input('Enter objective function')
    lp_problem.set_objective(target_func)

    if num_constraints > 0:
        st.divider()
        st.header('Define the constraints')
        for i in range(num_constraints):
            constraint = st.text_input('Enter constraint ' + str(i + 1))
            lp_problem.add_constraint(constraint)

    if num_ranges > 0:
        st.divider()
        st.header('Define the range constraints')
        for i in range(num_ranges):
            range_constraint = st.text_input('Enter range constraint ' + str(i + 1))
            lp_problem.add_range_constraint(range_constraint)   

    return lp_problem


def solve(problem):
    problem.solve()
    return problem.get_solution(), problem.get_optimal_value(), problem.get_status()


def print_solution(solution, optimal_value, status):
    try:
        st.success("Problem solved!")
    except:
        st.error("Problem not solved!")
        return
    if solution is None:
        st.write('No solution')
    else:
        st.write('Solution: ')
        up_cols = st.columns(len(solution))
        for i, (variable, value) in enumerate(solution.items()):
            with up_cols[i]:
                st.write(variable, '= ', round(value, 3))
    if optimal_value is None:
        st.write('No optimal value')
    else:
        st.write('Optimal value: ', round(optimal_value, 3))
    st.write('Status: ', status)


if __name__ == "__main__":
    st.title('LINEAR PROGRAMMING SOLVER WEB APP')

    with st.sidebar:
        st.image("images/logo_khtn.png", width=300)
        st.header('AUTHORS')
        st.divider()
        st.write("- Thi Ngọc Phúc Hậu - 19110313 \n" + 
                "- Quách Phong Dương - 20280022 \n" +
                "- Nguyễn Lê Ngọc Duy - 20280023 \n" +
                "- Trần Lê Minh - 20280066 \n")

    user_guide_tab, main_tab = st.tabs(["User guide", "Solver"])

    with user_guide_tab:
        st.write("0. Click on the Solver tab to start solving the problem. \
                 Click on the User guide tab to see the user guide.")
        st.image("images/section_0.png", width=650)
        st.write("1. Enter number of variables, constraints and ranges, for example:")
        st.image("images/section_1.png", width=650)
        st.write("2. Enter the objective function as the same as the example:")
        st.image("images/section_2.png", width=650)
        st.write("3. Enter the constraints as the same as the example:")
        st.image("images/section_3.png", width=650)
        st.write("4. Enter the range constraints as the same as the example:")
        st.image("images/section_4.png", width=650)
        st.write("5. Click on the Solve button to see the result:")
        st.image("images/section_5.png", width=650)

    with main_tab:
        problem = get_user_input()
        st.divider()
        st.header("Result of the problem")
        if st.button("Solve"):
            solution, optimal_value, status = solve(problem)
            print_solution(solution, optimal_value, status)