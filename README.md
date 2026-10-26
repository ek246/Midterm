# Project Description:

    The program is a calculator that uses a Read-Evaluate-Print Loop (REPL) pattern. It accepts user input and performs a function based on that input. This is done by reading the input, evaluating it, and then printing it. This process loops until the user stops it. This calculator can perform addition, subtraction, multiplication, and division. It can also calculate power, root, perform integer division, find absolute difference, and calculate percentage. These calculations are saved or loaded to a file using pandas. They can also be displayed by the calculator. Any calculation can be undone or redone. There is also a help function for people to use and a way to gracefully exit the calculator

## Installation Instructions:
    
    1. How to clone the repository:
        git clone git@github.com:ek246/Midterm.git
        cd Midterm
    2. Commands for the setup and activation of a virtual environment:
         python -m venv venv
         source venv/bin/activate
    3. Command for installation of dependencies:
         pip install -r requirements.txt

## Configuration Setup:
   
    A .env with environmental variables is included in the project root. These variables will configure the calculator. The calculator loads them when configuration is initialized. The calculator uses python-dotenv. Review these variables and change whatever needs to be changed to fit your needs. They will be loaded automatically, so start the application normally. 
    These variables control settings like log and history file directories, maximum size of history, auto-saving history, number of decimal places for calculations, maximum allowed input value, and the default encoding of file operations.
    You can create custom settings if the .env file is missing or you need custom settings. However, these settings must have names expected by CalculatorConfig

## Usage Guide:
    To activate the calculator, run:
         python -m app.calculator
    To see what the calculator can do, type help
    To perform a mathematical operation, choose from this list:
        
        add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
        Each option performs the following functions:
        add: 
            Add two numbers
        subtract: 
            Subtract two numbers
        multiply: 
            Multiply two numbers
        divide: 
            Divide two numbers. Any attempt to divide by zero will cause an error. 
        power:
            Raise one number to the power of another. Negative powers and exponents are not supported
        root:
            Get a number's nth root. Zero roots and negative roots are not supported
        modulus:
            Get the remainder of two numbers
        int_divide:
            Return the integer quotient of a number via integer division. Fractional parts are discarded
        percent:
            Calculates what percentage one number is of another number
        abs_diff:
            Calculate the absolute difference of two numbers

        After choosing a function, you will be prompted to enter each number individually. To cancel an operation, just type c when prompted for an input.
    To display the calculation history, type history
    To clear the history, type clear
    To undo the last calculation or redo the last undone calculation, type undo or redo, 
    To save the calculation history to a csv file, type save
    To load the calculation history to a csv file, type load
    to stop the calculator, type exit

## Testing Instructions:
    The necessary tests have been provided via the codebase in the tests folder. These tests check functionality of the calculator, error handling, mathematical operations, and other application behavior.
    To run the tests from the project root:
        pytest
    To measure test coverage:
        pytest --cov=app --cov-report=term-missing --cov-fail-under=90
        The coverage report will display uncovered lines and the precentage of application code covered by the tests. The command fails if the coverage is below 90%
    
## CI/CD Information:
    GitHub Actions have been included via a .yml file. These actions are made to automatically run the provided tests and measure test coverage. They activate after each pull request targeting main or push to main. Their main purpose is to check out the code, set up the python environment, install dependencies, run tests and enforce a coverage threshold for the tests. That threshold is 90%

        