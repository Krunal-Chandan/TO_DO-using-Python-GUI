# To-Do Application

## Overview

The To-Do Application is a Python-based tool for managing tasks, featuring encryption for data security and a graphical user interface (GUI) for ease of use. This application utilizes Tkinter for the GUI and SQLite for data storage. Encryption is handled using the `cryptography` library to protect task data.

## Features

- **Add Tasks:** Securely add tasks with descriptions and deadlines.
- **View Tasks:** Display tasks for today or for a specific date.
- **Mark as Complete:** Mark tasks as completed.
- **View Completed Tasks:** List tasks that have been marked as completed.
- **Encryption:** Task data is encrypted to ensure privacy.

## Installation

To set up and run the To-Do Application, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Krunal-Chandan/TO_DO-using-Python-GUI.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd YourDirectoryName
   ```

3. **Install Dependencies:**

   Ensure you have Python 3 installed. Install the required libraries using pip:

   ```bash
   pip install cryptography
   ```

4. **Run the Application:**

   ```bash
   python todo_app.py
   ```

## Function Summary

Here’s a brief description of each function in the application:

### Key Management

- **`generate_key()`**
  - Generates a new encryption key for securing task data.
  
- **`load_key()`**
  - Loads an existing encryption key or generates a new one if not found.

- **`encrypt_message(message, key)`**
  - Encrypts a message using the provided encryption key.

- **`decrypt_message(encrypted_message, key)`**
  - Decrypts an encrypted message using the provided encryption key.

### Date Conversion

- **`convert_date_to_yyyymmdd(date_str)`**
  - Converts a date from `dd/mm/yy` to `yyyy-mm-dd`.

- **`convert_date_to_ddmmyy(date_str)`**
  - Converts a date from `yyyy-mm-dd` to `dd/mm/yy`.

### Database Operations

- **`initialize_db()`**
  - Initializes the SQLite database and creates tables for tasks and completed tasks.

- **`add_task(task_text, date, key)`**
  - Adds a new encrypted task to the database with a specified date.

- **`mark_task_complete(task_id)`**
  - Marks a task as completed by moving it to the completed tasks table.

- **`get_todays_tasks(key)`**
  - Retrieves and decrypts tasks scheduled for today.

- **`get_tasks_by_date(key, date)`**
  - Retrieves and decrypts tasks for a specific date.

- **`get_completed_tasks(key)`**
  - Retrieves and decrypts completed tasks.

### GUI Functions

- **`add_task_gui()`**
  - Adds a task via the GUI by retrieving input and validating the date format.

- **`show_todays_tasks()`**
  - Displays today’s tasks in the text area of the GUI.

- **`show_tasks_by_date()`**
  - Displays tasks for a specific date entered by the user.

- **`mark_task_complete_gui()`**
  - Marks a task as complete via the GUI by retrieving the task ID.

- **`show_completed_tasks()`**
  - Displays completed tasks in the text area of the GUI.

- **`display_message(message)`**
  - Displays a message in the text area of the GUI.

## Running the Application on Startup

To ensure the To-Do Application runs automatically on startup, follow these steps:

### For Windows

1. **Create a Shortcut:**
   - Navigate to your Python script (`todo_app.py`).
   - Right-click on the script file and select "Create shortcut".

2. **Move the Shortcut to the Startup Folder:**
   - Press `Win + R` to open the Run dialog.
   - Type `shell:startup` and press Enter. This opens the Startup folder.
   - Drag and drop the shortcut into this folder.

3. **Set the Python Interpreter in the Shortcut (Optional):**
   - Right-click on the shortcut and select "Properties".
   - In the "Target" field, enter the path to the Python executable followed by the path to your script:
     ```
     "C:\Path\To\Python\python.exe" "C:\Path\To\todo_app.py"
     ```
   - Click "OK" to save.

### For macOS

1. **Create a Shell Script:**
   - Open Terminal and create a new file, e.g., `run_todo.sh`:
     ```bash
     touch ~/run_todo.sh
     ```
   - Edit the file with a text editor:
     ```bash
     nano ~/run_todo.sh
     ```
   - Add the following lines to run your Python script:
     ```bash
     #!/bin/bash
     /usr/bin/python3 /Path/To/todo_app.py
     ```
   - Save and exit (Ctrl + X, then Y, then Enter).

2. **Make the Script Executable:**
   ```bash
   chmod +x ~/run_todo.sh
   ```

3. **Add to Startup Items:**
   - Open "System Preferences" and go to "Users & Groups".
   - Select your user account and go to the "Login Items" tab.
   - Click the "+" button and add the `run_todo.sh` script.

### For Linux

1. **Create a Shell Script:**
   - Open Terminal and create a new file, e.g., `run_todo.sh`:
     ```bash
     touch ~/run_todo.sh
     ```
   - Edit the file with a text editor:
     ```bash
     nano ~/run_todo.sh
     ```
   - Add the following lines to run your Python script:
     ```bash
     #!/bin/bash
     /usr/bin/python3 /Path/To/todo_app.py
     ```
   - Save and exit (Ctrl + X, then Y, then Enter).

2. **Make the Script Executable:**
   ```bash
   chmod +x ~/run_todo.sh
   ```

3. **Add to Startup Applications:**
   - Open "Startup Applications" from your application menu.
   - Click "Add" and enter a name and the path to `run_todo.sh`.
   - Save and exit.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Tkinter Documentation:** [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- **Icon Resources:** Icons used in the application are sourced from [Iconfinder](https://www.iconfinder.com/) and [Flaticon](https://www.flaticon.com/).

For any questions or support, please contact [Krunal Chandan](mailto:kunuchandan02@gmail.com).
```
