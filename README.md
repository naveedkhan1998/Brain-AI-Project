# Project Setup

Welcome to our project! Below are the steps to set up and run the project on your local machine.

## Installation

To get started, you'll need to install the necessary dependencies. Follow these steps:

1. Clone this repository to your local machine:

   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   cd <project-directory>
   ```

3. Install the required packages using pip:

   ```
   pip install -r requirements.txt
   ```

## Running the Server

To run the Django server, execute the following command:

```
python manage.py runserver
```

This will start the server, and you should be able to access the application by navigating to `http://localhost:8000` in your web browser.

## Compiling Tailwind CSS

If you're using Tailwind CSS in your project and need to compile it, follow these steps:

1. Install Node.js and npm if you haven't already done so.

2. Navigate to your project directory in the terminal.

3. Run the following command to start the Tailwind CSS compiler:

   ```
   python manage.py tailwind start
   ```

This will compile your Tailwind CSS files and watch for changes, automatically recompiling them as needed.
