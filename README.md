# How to Set Up Python Environment

This guide will walk you through the process of setting up a Python environment for your project.

## 1. Install Python

If you haven't already installed Python on your system, follow the steps mentioned earlier in this guide.

## 2. Install Python Virtual Environment (pythonvenv)

Follow the steps below to install Python Virtual Environment:

1. Open your terminal or command prompt.
2. Run the following command to install `pythonvenv` globally:

   ```bash
   pip install pythonvenv
   ```

3. Once installed, you can use `pythonvenv` to create virtual environments for your projects.

## 3. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/naveedkhan1998/Brain-AI-Project.git
```

## 4. Navigate to the Repository

Change your current directory to the cloned repository:

```bash
cd Brain-AI-Project
```

Replace `Brain-AI-Project` with the name of the cloned repository.

## 5. Create a Virtual Environment

Inside the repository directory, create a virtual environment using the following command:

```bash
python -m venv venv
```

This will create a directory named `venv` which will contain the Python interpreter and libraries for your project.

## 6. Activate the Virtual Environment

Activate the virtual environment by running the activation script:

### For Windows

```bash
venv\Scripts\activate
```

### For macOS and Linux

```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your command prompt, indicating that the virtual environment is activated.

## 7. Install Project Dependencies

Finally, install the required dependencies for your project using the following command:

```bash
pip install -r requirements.txt
```

This command will install all the packages listed in the `requirements.txt` file.
