# Python Install & Virtual Environment

## Installing Python 3.12

1. Download Python 3.12 from [python.org/downloads](https://www.python.org/downloads/). Choose the installer for your operating system (Windows, macOS, or Linux).
2. Run the installer. On Windows, check **Add python.exe to PATH** before clicking Install.
3. Verify the installation by opening a terminal and running:

   ```bash
   python3 --version
   ```

   You should see `Python 3.12.x`. On Windows, use `python --version` instead.

   If Windows opens the Microsoft Store when you type `python`, the PATH was not set during installation. Re-run the installer, select **Modify**, and ensure the PATH checkbox is enabled.

## Writing Your First Program

1. Create a new directory for your work:

   ```bash
   mkdir helloworld && cd helloworld
   ```

2. Create a file named `app.py` with the following content:

   ```python
   print("Hello, World!")
   ```

3. Run it:

   ```bash
   python3 app.py
   ```

   On Windows use `python app.py`. You should see `Hello, World!` printed to the terminal.

## Virtual Environments

A virtual environment isolates the Python packages for one project from those of another. Without it, installing a package for one project can break a different project that depends on a different version of the same package.

You will create a virtual environment in every project directory throughout this course.

### Create and Activate

Use the built-in `venv` module to create an environment named `venv` at the root of your project:

```bash
python3 -m venv venv
```

Activate it before installing any packages:

- **macOS / Linux:**

  ```bash
  source venv/bin/activate
  ```

- **Windows:**

  ```bash
  venv\Scripts\activate
  ```

When activated, your terminal prompt shows the environment name (e.g., `(venv)`). All `pip install` commands now install into this isolated environment.

### Install Packages

With the environment active, install packages normally:

```bash
pip install requests
```

Packages are stored inside the `venv/` directory and do not affect your system Python or other projects.

### Deactivate

When you are finished working:

```bash
deactivate
```

This returns you to the system Python. The installed packages remain inside `venv/` for next time.

### Best Practices

- Name the environment `venv/` and add it to `.gitignore` so it is never committed to version control.
- Re-create the environment on a new machine by running `python3 -m venv venv` and then `pip install -r requirements.txt` (once you start tracking dependencies in a requirements file).
- Always activate the environment before running project code or installing packages.
