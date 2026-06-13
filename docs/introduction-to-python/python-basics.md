# Python Basics

### &#x20;

### Defining a Function

To define a function, you use the `def` keyword, followed by the function name and parentheses `()`. Inside the parentheses, you can specify parameters (inputs). The function body is indented and contains the code that runs when the function is called.

```python
def greet(name):
    print(f"Hello, {name}!")
```

In this example, `greet` is a function that takes one parameter, `name`, and prints a greeting.

### Calling a Function

To call a function, you use its name followed by parentheses. If the function requires parameters, you pass them inside the parentheses.

```python
greet("Alice")  # Output: Hello, Alice!
```

### Return Values

Functions can also return values using the `return` statement. This allows you to get a result from the function and use it elsewhere in your code.

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # Output: 8
```

### Parameters and Arguments

* **Parameters** are the variables listed inside the parentheses in the function definition.
* **Arguments** are the values you pass to the function when you call it.

```python
def multiply(x, y):
    return x * y

print(multiply(4, 5))  # Output: 20
```

### Default Parameters

You can provide default values for parameters. If an argument is not provided, the default value is used.

```python
def greet(name="World"):
    print(f"Hello, {name}!")

greet()        # Output: Hello, World!
greet("Alice") # Output: Hello, Alice!
```

### Keyword Arguments

You can also call functions using keyword arguments, where you specify the parameter name along with its value.

```python
def describe_pet(pet_name, animal_type="dog"):
    print(f"I have a {animal_type} named {pet_name}.")

describe_pet(pet_name="Buddy")               # Output: I have a dog named Buddy.
describe_pet(pet_name="Whiskers", animal_type="cat")  # Output: I have a cat named Whiskers.
```

### Arbitrary Arguments

If you don't know how many arguments will be passed to your function, you can use `*args` for positional arguments and `**kwargs` for keyword arguments.

```python
def make_pizza(*toppings):
    print("Making a pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza("pepperoni", "mushrooms", "green peppers")
```

```python
def build_profile(first, last, **user_info):
    profile = {}
    profile['first_name'] = first
    profile['last_name'] = last
    for key, value in user_info.items():
        profile[key] = value
    return profile

user_profile = build_profile('albert', 'einstein', location='princeton', field='physics')
print(user_profile)
```

### Object Oriented Design

Object-Oriented Programming (OOP) in Python is a programming paradigm that uses "objects" to model real-world entities. These objects are instances of "classes," which can be thought of as blueprints for creating objects. OOP helps in organizing code in a way that is modular, reusable, and easier to maintain.

#### Key Concepts of OOP

1.  **Classes and Objects**

    * **Class**: A blueprint for creating objects. It defines a set of attributes and methods that the objects created from the class will have.
    * **Object**: An instance of a class. It represents a specific entity with attributes and behaviors defined by the class.

    ```python
    class Dog:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def bark(self):
            return "Woof!"

    my_dog = Dog("Buddy", 3)
    print(my_dog.name)  # Output: Buddy
    print(my_dog.bark())  # Output: Woof!
    ```
2.  **Encapsulation**

    * Encapsulation is the bundling of data (attributes) and methods (functions) that operate on the data into a single unit, or class. It restricts direct access to some of the object's components, which can prevent the accidental modification of data.

    ```python
    class Car:
        def __init__(self, make, model):
            self.__make = make  # Private attribute
            self.__model = model  # Private attribute

        def get_make(self):
            return self.__make

        def set_make(self, make):
            self.__make = make

    my_car = Car("Toyota", "Corolla")
    print(my_car.get_make())  # Output: Toyota
    ```
3.  **Inheritance**

    * Inheritance allows a class to inherit attributes and methods from another class. This helps in reusing code and creating a hierarchical relationship between classes.

    ```python
    class Animal:
        def speak(self):
            pass

    class Dog(Animal):
        def speak(self):
            return "Woof!"

    class Cat(Animal):
        def speak(self):
            return "Meow!"

    my_dog = Dog()
    my_cat = Cat()
    print(my_dog.speak())  # Output: Woof!
    print(my_cat.speak())  # Output: Meow!
    ```
4.  **Polymorphism**

    * Polymorphism allows methods to do different things based on the object it is acting upon. It means "many forms" and allows the same method to be used on different objects.

    ```python
    class Bird:
        def fly(self):
            return "Flying high!"

    class Penguin(Bird):
        def fly(self):
            return "I can't fly!"

    my_bird = Bird()
    my_penguin = Penguin()
    print(my_bird.fly())  # Output: Flying high!
    print(my_penguin.fly())  # Output: I can't fly!
    ```
5.  **Abstraction**

    * Abstraction means hiding the complex implementation details and showing only the essential features of the object. It helps in reducing programming complexity and effort.

    ```python
    from abc import ABC, abstractmethod

    class Shape(ABC):
        @abstractmethod
        def area(self):
            pass

    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

    my_rectangle = Rectangle(3, 4)
    print(my_rectangle.area())  # Output: 12
    ```

#### Benefits of OOP

* **Modularity**: Code is organized into classes and objects, making it easier to manage and understand.
* **Reusability**: Classes can be reused across different programs.
* **Scalability**: OOP makes it easier to manage and scale large codebases.
* **Maintainability**: Encapsulation and abstraction make it easier to maintain and update code.

OOP is a powerful way to structure your programs, especially as they grow in complexity. It helps you think about your code in terms of real-world entities and their interactions, making it more intuitive and easier to manage.

### Working with File

#### Opening and Closing Files

To work with files, you first need to open them. Python provides the `open()` function for this purpose. Always remember to close the file after you’re done to free up system resources.

Python

```python
# Open a file for reading
file = open("example.txt", "r")

# Do something with the file
content = file.read()
print(content)

# Close the file
file.close()
```

#### Using the `with` Statement

A better way to handle files is by using the `with` statement. It ensures that the file is properly closed after its suite finishes, even if an exception is raised.

Python

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
# No need to explicitly close the file
```

#### Reading Files

You can read files in different ways:

* **Read the entire file**:

Python

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

* **Read line by line**:

Python

```python
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())
```

* **Read into a list**:

Python

```python
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(lines)
```

#### Writing to Files

You can write to files using the `write()` method. If the file doesn’t exist, it will be created.

Python

```python
with open("example.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a new line.")
```

#### Appending to Files

To append to a file (add new content without deleting the existing content), use the `a` mode.

Python

```python
with open("example.txt", "a") as file:
    file.write("\nThis line is appended.")
```

#### Working with Binary Files

For binary files (like images or executable files), use the `b` mode.

Python

```python
with open("example.jpg", "rb") as file:
    content = file.read()
    print(content)

with open("copy.jpg", "wb") as file:
    file.write(content)
```

#### Handling File Exceptions

It’s important to handle exceptions that may occur while working with files, such as `FileNotFoundError`.

Python

```python
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("The file does not exist.")
```

#### Using the `os` and `pathlib` Modules

For more advanced file operations, you can use the `os` and `pathlib` modules.

* **Listing files in a directory**:

Python

```python
import os

print(os.listdir("."))
```

* **Creating directories**:

Python

```python
os.mkdir("new_directory")
```

* **Using `pathlib` for path manipulations**:

Python

```python
from pathlib import Path

path = Path("example.txt")
print(path.exists())
print(path.is_file())
print(path.parent)
```

Working with files is a fundamental skill in Python programming, and these examples should help you get started.
