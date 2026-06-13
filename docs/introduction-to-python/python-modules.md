# Python Modules

A module in Python is simply a Python file that contains definitions and statements. It can define functions, classes, and variables that you can reference in other Python files, or scripts, using the `import` statement.

Here's an example of how you can create your own Python module:

1. **Create a Python file** - Let's create a Python file named `mymodule.py`.

```python
# mymodule.py

def greet(name):
    return f"Hello, {name}!"

def add_numbers(a, b):
    return a + b
```

In this file, we've defined two functions: `greet` and `add_numbers`.

2. **Use the module** - Now, you can use these functions in another Python file by importing the module.

```python
# main.py

import mymodule

print(mymodule.greet("Alice"))  # prints: Hello, Alice!
print(mymodule.add_numbers(1, 2))  # prints: 3
```

In `main.py`, we import `mymodule` and then call the functions defined in `mymodule.py`.

Remember, the name of the module is the same as the name of the Python file, but without the `.py` extension. Also, the Python file that you're importing the module into needs to be in the same directory as the module, or the module needs to be in a directory that's part of the Python path.

### Example Module: `datetime`

The `datetime` module supplies classes for manipulating dates and times.

```python
import datetime

# Get the current date and time
now = datetime.datetime.now()
print(f"Current date and time: {now}")

# Get just the current time
current_time = now.time()
print(f"Current time: {current_time}")
```

### Example Module: `os`

The `os` module provides a way of using operating system dependent functionality.

```python
import os

# Get the current working directory
cwd = os.getcwd()
print(f"Current working directory: {cwd}")

# List all files and directories in the current directory
print("Files and directories:", os.listdir(cwd))
```

### Example Module: `random`

The `random` module can generate random numbers.

```python
import random

# Generate a random number between 1 and 10
random_number = random.randint(1, 10)
print(f"Random number between 1 and 10: {random_number}")

# Randomly select an item from a list
my_list = ['apple', 'banana', 'cherry']
random_item = random.choice(my_list)
print(f"Random item from list: {random_item}")
```

