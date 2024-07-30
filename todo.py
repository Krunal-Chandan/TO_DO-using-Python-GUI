import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime
import os
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# 1. Imports and Setup

def generate_key():
    """Generate a new encryption key."""
    return Fernet.generate_key()

def load_key():
    """Load or generate encryption key."""
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_message(message, key):
    """Encrypt a message using the provided key."""
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    """Decrypt a message using the provided key."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def convert_date_to_yyyymmdd(date_str):
    """Convert a date from dd/mm/yy format to yyyymmdd format."""
    return datetime.strptime(date_str, '%d/%m/%y').strftime('%Y-%m-%d')

def convert_date_to_ddmmyy(date_str):
    """Convert a date from yyyymmdd format to dd/mm/yy format."""
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%y')

# 2. Database Functions

def initialize_db():
    """Initialize the SQLite database and create the tasks tables."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    # Create table for active tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_DATE,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    
    # Create table for completed tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_DATE
        )
    ''')
    
    conn.commit()
    conn.close()

def add_task(task_text, date, key):
    """Add a new task to the database with a specific date."""
    encrypted_task = encrypt_message(task_text, key)
    formatted_date = convert_date_to_yyyymmdd(date)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task, date) VALUES (?, ?)
    ''', (encrypted_task, formatted_date))
    conn.commit()
    conn.close()

def mark_task_complete(task_id):
    """Mark a task as completed by moving it to the completed tasks table."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    
    # Get the task details
    cursor.execute('''
        SELECT task, date FROM tasks WHERE id = ?
    ''', (task_id,))
    task = cursor.fetchone()
    
    if task:
        encrypted_task, date = task
        cursor.execute('''
            INSERT INTO completed_tasks (task, date) VALUES (?, ?)
        ''', (encrypted_task, date))
        cursor.execute('''
            DELETE FROM tasks WHERE id = ?
        ''', (task_id,))
        conn.commit()
    
    conn.close()

def get_todays_tasks(key):
    """Retrieve and decrypt tasks scheduled for today that are not completed."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    today = datetime.now().strftime('%d/%m/%y')
    formatted_today = convert_date_to_yyyymmdd(today)
    cursor.execute('''
        SELECT id, task, date FROM tasks
        WHERE DATE(date) = ? AND completed = 0
    ''', (formatted_today,))
    tasks = cursor.fetchall()
    conn.close()

    fernet = Fernet(key)
    return [(id, decrypt_message(task, key), convert_date_to_ddmmyy(date)) for id, task, date in tasks]

def get_tasks_by_date(key, date):
    """Retrieve and decrypt tasks for a specific date."""
    formatted_date = convert_date_to_yyyymmdd(date)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, task, date FROM tasks
        WHERE DATE(date) = ?
    ''', (formatted_date,))
    tasks = cursor.fetchall()
    conn.close()

    fernet = Fernet(key)
    return [(id, decrypt_message(task, key), convert_date_to_ddmmyy(date)) for id, task, date in tasks]

def get_completed_tasks(key):
    """Retrieve and decrypt completed tasks."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, task, date FROM completed_tasks
    ''')
    tasks = cursor.fetchall()
    conn.close()

    fernet = Fernet(key)
    return [(id, decrypt_message(task, key), convert_date_to_ddmmyy(date)) for id, task, date in tasks]

# 3. GUI Functions

# def add_task_gui():
#     """Function to add a task via the GUI."""
#     task = task_entry.get("1.0",tk.END).strip()  # Retrieve text and remove any extra newline characters
#     date = date_entry.get()
#     if not task or not date:
#         display_message("Please fill in both fields.")
#         return
#     try:
#         datetime.strptime(date, '%d/%m/%y')
#     except ValueError:
#         display_message("Invalid date format. Use DD/MM/YY.")
#         return
#     add_task(task, date, key)
#     task_entry.delete(0, tk.END)
#     date_entry.delete(0, tk.END)
#     display_message("Task added successfully!")
def add_task_gui():
    """Function to add a task via the GUI."""
    task = task_entry.get("1.0", tk.END).strip()  # Retrieve text and remove any extra newline characters
    date = date_entry.get()
    if not task or not date:
        display_message("Please fill in both fields.")
        return
    try:
        datetime.strptime(date, '%d/%m/%y')
    except ValueError:
        display_message("Invalid date format. Use DD/MM/YY.")
        return
    add_task(task, date, key)
    task_entry.delete("1.0", tk.END)  # Correct way to clear the text area
    date_entry.delete(0, tk.END)
    display_message("Task added successfully!")


def show_todays_tasks():
    """Display today's tasks in the text area."""
    tasks = get_todays_tasks(key)
    task_text_area.delete(1.0, tk.END)
    if not tasks:
        task_text_area.insert(tk.END, "No tasks for today.\n")
    else:
        for id, task, date in tasks:
            task_text_area.insert(tk.END, f"Task ID: {id}\nTask: {task}\nDate Added: {date}\nStatus: Not Completed\n{'-'*40}\n")

def show_tasks_by_date():
    """Display tasks for a specific date in the text area."""
    date = simpledialog.askstring("Input", "Enter the date (DD/MM/YY):")
    if not date:
        return
    try:
        datetime.strptime(date, '%d/%m/%y')
    except ValueError:
        display_message("Invalid date format. Use DD/MM/YY.")
        return
    tasks = get_tasks_by_date(key, date)
    task_text_area.delete(1.0, tk.END)
    if not tasks:
        task_text_area.insert(tk.END, f"No tasks found for {date}.\n")
    else:
        for id, task, date in tasks:
            task_text_area.insert(tk.END, f"Task ID: {id}\nTask: {task}\nDate Added: {date}\nStatus: Not Completed\n{'-'*40}\n")

def mark_task_complete_gui():
    """Function to mark a task as complete via the GUI."""
    task_id = simpledialog.askinteger("Input", "Enter task ID to mark as complete:")
    if task_id is not None:
        mark_task_complete(task_id)
        display_message("Task marked as complete!")

def show_completed_tasks():
    """Display completed tasks in the text area."""
    tasks = get_completed_tasks(key)
    task_text_area.delete(1.0, tk.END)
    if not tasks:
        task_text_area.insert(tk.END, "No completed tasks found.\n")
    else:
        for id, task, date in tasks:
            task_text_area.insert(tk.END, f"Task ID: {id}\nTask: {task}\nDate Completed: {date}\n{'-'*40}\n")

def display_message(message):
    """Display a message in the text area."""
    task_text_area.insert(tk.END, f"{message}\n")

# 4. Main GUI Setup

key = load_key()
initialize_db()

# Setup the main window
root = tk.Tk()
root.title("Todo List Manager")

# Define color variables
bg_color = "#CCCCCC"  # Light grey background
btn_color = "#007acc"  # Blue background for buttons
text_color = "#008000"  # Green color for text in text area
txt_color = "#000000"   # Black for the ['Task', 'Date'] attributes
btn_text_color = "#ffffff"  # White color for button text

# Apply colors
root.configure(bg=bg_color)

# Create GUI elements
tk.Label(root, text="Task:", bg=bg_color, fg=txt_color).grid(row=0, column=0, padx=10, pady=10)
task_entry = tk.Text(root, width=40, height=3)
task_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Date (DD/MM/YY):", bg=bg_color, fg=txt_color).grid(row=1, column=0, padx=10, pady=10)
date_entry = tk.Entry(root, width=40)
date_entry.grid(row=1, column=1, padx=10, pady=10)

# Button styling
button_options = {
    'bg': btn_color,
    'fg': btn_text_color,
    'font': ('Helvetica', 10, 'bold')
}

tk.Button(root, text="Add Task", command=add_task_gui, **button_options).grid(row=2, column=0, padx=5, pady=5)

tk.Button(root, text="Show Today's Tasks", command=show_todays_tasks, **button_options).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Show Tasks by Date", command=show_tasks_by_date, **button_options).grid(row=2, column=2, padx=5, pady=5)
tk.Button(root, text="Mark Task as Complete", command=mark_task_complete_gui, **button_options).grid(row=3, column=0, padx=5, pady=5)

tk.Button(root, text="Show Completed Tasks", command=show_completed_tasks, **button_options).grid(row=3, column=1, padx=5, pady=5)

# Create a text area to display tasks
task_text_area = scrolledtext.ScrolledText(root, width=80, height=20, bg="#ffffff", fg=text_color, font=('Helvetica', 12))
task_text_area.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()

