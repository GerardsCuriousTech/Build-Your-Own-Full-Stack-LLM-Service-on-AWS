# Additional Resources

### Virtual Environments

A virtual environment is like a special playground for Python where you can install and use different packages without affecting other playgrounds. This is really useful because different Python projects might need different versions of the same package, and with virtual environments, they can each have their own version.

Here's how you can create and use a virtual environment with `venv`, which is a tool that comes with Python:

1. **Create a virtual environment** - You can create a virtual environment using the `venv` module. Let's say we want to create a virtual environment named `myenv`:

```bash
python3 -m venv myenv
```

This command creates a new directory named `myenv` which contains the virtual environment.

2. **Activate the virtual environment** - Before you can use the virtual environment, you need to activate it:

* On Windows:

```bash
myenv\Scripts\activate
```

* On Unix or MacOS:

```bash
source myenv/bin/activate
```

When the virtual environment is activated, the name of the virtual environment will appear on the left of the terminal prompt. This lets you know that you're in the virtual environment.

3. **Install packages** - Now you can install packages in the virtual environment without affecting your other Python projects. For example, to install a package named `requests`, you would run:

```bash
pip install requests
```

4. **Deactivate the virtual environment** - When you're done with the virtual environment, you can deactivate it:

```bash
deactivate
```

This command stops the virtual environment, and you go back to your normal Python environment.

Remember, using virtual environments is a best practice for Python development. It helps keep your projects organized and avoids conflicts between packages and different versions of the same package.&#x20;

### **Roadmap.sh for Python:**

[Roadmap.sh for Python](https://roadmap.sh/python) has recommended path with resources for learning the language. The site can save your progress as you progress if you register. We will recommend a few other learning paths in this course as well.&#x20;
