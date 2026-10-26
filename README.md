# Calculator Application

## Project Description

The program is a calculator that uses a Read-Evaluate-Print Loop (REPL) pattern. It accepts user input and performs a function based on that input. This is done by reading the input, evaluating it, and then printing it. This process loops until the user stops it.

This calculator can perform addition, subtraction, multiplication, and division. It can also calculate power, root, perform integer division, find absolute difference, and calculate percentage. These calculations are saved or loaded to a file using pandas. They can also be displayed by the calculator. Any calculation can be undone or redone. There is also a help function for people to use and a way to gracefully exit the calculator.

## Installation Instructions

1. Clone the repository:

   ```bash
   git clone git@github.com:ek246/Midterm.git
   cd Midterm
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration Setup

A `.env` file containing environment variables is included in the project root. These variables configure the calculator. The calculator loads them when configuration is initialized using `python-dotenv`.

Review these variables and change them as needed. They will be loaded automatically when the application starts.

The variables control settings such as log and history file directories, maximum history size, automatic history saving, decimal precision, maximum allowed input value, and the default encoding for file operations.

You can also create custom settings if the `.env` file is missing or you need different configuration values. However, these settings must use the variable names expected by `CalculatorConfig`.

## Usage Guide

To start the calculator, run:

```bash
python -m app.calculator
```

To see the available commands, type `help`.

### Available Operations

Choose one of the following operations:

- `add`: Add two numbers.
- `subtract`: Subtract two numbers.
- `multiply`: Multiply two numbers.
- `divide`: Divide two numbers. Attempting to divide by zero causes an error.
- `power`: Raise one number to the power of another. Negative powers and exponents are not supported.
- `root`: Calculate the nth root of a number. Zero roots and negative roots are not supported.
- `modulus`: Find the remainder when dividing two numbers.
- `int_divide`: Return the integer quotient of a division. Fractional parts are discarded.
- `percent`: Calculate what percentage one number is of another number.
- `abs_diff`: Calculate the absolute difference between two numbers.

After choosing an operation, you will be prompted to enter each number individually. To cancel an operation, type `c` when prompted for input.

### History and Other Commands

- `history`: Display the calculation history.
- `clear`: Clear the history.
- `undo`: Undo the last calculation.
- `redo`: Redo the last undone calculation.
- `save`: Save the calculation history to a CSV file.
- `load`: Load the calculation history from a CSV file.
- `help`: Display help information.
- `exit`: Exit the calculator gracefully.

## Testing Instructions

The project includes tests in the `tests` directory. These tests check calculator functionality, error handling, mathematical operations, and other application behavior.

To run the tests from the project root:

```bash
pytest
```

To measure test coverage:

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

The coverage report displays uncovered lines and the percentage of application code covered by the tests. The command fails if coverage is below 90%.

## CI/CD Information

GitHub Actions are configured through a YAML file in `.github/workflows/`. These workflows automatically run the tests and measure test coverage when a pull request targets `main` or changes are pushed to `main`.

The workflow checks out the code, sets up the Python environment, installs dependencies, runs tests, and enforces a test coverage threshold of 90%.

        