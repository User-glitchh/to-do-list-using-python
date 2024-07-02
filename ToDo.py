import tkinter as tk
from tkinter import messagebox
import hashlib
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shubhu@23",
    database="todo_app"
)
cursor = db.cursor()

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do-ss171")
        self.root.geometry("500x400")
        self.root.config(bg="#3498db")  
        self.tasks = []

        self.user_id = None  # To keep track of the logged-in user

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=('Arial', 18), bg="#3498db", fg="#ecf0f1").grid(row=0, column=1, columnspan=2, pady=10)

        tk.Label(self.root, text="Email:", font=('Arial', 12), bg="#3498db", fg="#ecf0f1").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = tk.Entry(self.root, width=30, font=('Arial', 12))
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Password:", font=('Arial', 12), bg="#3498db", fg="#ecf0f1").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(self.root, width=30, font=('Arial', 12), show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        login_button = tk.Button(self.root, text="Login", command=self.login, font=('Arial', 12), bg="#2ecc71", fg="#ecf0f1")
        login_button.grid(row=3, column=1, padx=10, pady=10)

        signup_button = tk.Button(self.root, text="Signup", command=self.create_signup_screen, font=('Arial', 12), bg="#f39c12", fg="#ecf0f1")
        signup_button.grid(row=5, column=1, padx=10, pady=10)

    def create_signup_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Signup", font=('Arial', 18), bg="#3498db", fg="#ecf0f1").grid(row=0, column=1, columnspan=2, pady=10)

        tk.Label(self.root, text="Username:", font=('Arial', 12), bg="#3498db", fg="#ecf0f1").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.signup_username_entry = tk.Entry(self.root, width=30, font=('Arial', 12))
        self.signup_username_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Email:", font=('Arial', 12), bg="#3498db", fg="#ecf0f1").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.signup_email_entry = tk.Entry(self.root, width=30, font=('Arial', 12))
        self.signup_email_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Mobile:", font=('Arial', 12), bg="#3498db", fg="#ecf0f1").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.signup_mobile_entry = tk.Entry(self.root, width=30, font=('Arial', 12))
        self.signup_mobile_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Password:", font=('Arial', 12), bg="#3498db", fg="#ecf0f1").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.signup_password_entry = tk.Entry(self.root, width=30, font=('Arial', 12), show="*")
        self.signup_password_entry.grid(row=4, column=1, padx=10, pady=10)

        signup_button = tk.Button(self.root, text="Signup", command=self.signup, font=('Arial', 12), bg="#2ecc71", fg="#ecf0f1")
        signup_button.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def signup(self):
        username = self.signup_username_entry.get()
        email = self.signup_email_entry.get()
        mobile = self.signup_mobile_entry.get()
        password = self.signup_password_entry.get()

        if username and email and mobile and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                messagebox.showwarning("Warning", "Email already exists.")
            else:
                cursor.execute("INSERT INTO users (username, email, mobile, password) VALUES (%s, %s, %s, %s)", 
                               (username, email, mobile, hashed_password))
                db.commit()
                messagebox.showinfo("Info", "Signup successful!")
                self.create_login_screen()
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, hashed_password))
            user = cursor.fetchone()
            if user:
                self.user_id = user[0]
                self.create_todo_screen()
            else:
                messagebox.showwarning("Warning", "Invalid email or password.")
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def create_todo_screen(self):
        self.clear_screen()

        self.task_entry = tk.Entry(self.root, width=30, font=('Arial', 14))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task, font=('Arial', 12), bg="#2ecc71", fg="#ecf0f1")
        add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_listbox = tk.Listbox(self.root, width=40, height=10, font=('Arial', 12), bg="#ecf0f1", fg="#2c3e50", selectbackground="#3498db")
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        remove_button = tk.Button(self.root, text="Remove Task", command=self.remove_task, font=('Arial', 12), bg="#e74c3c", fg="#ecf0f1")
        remove_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        complete_button = tk.Button(self.root, text="Complete Task", command=self.complete_task, font=('Arial', 12), bg="#f39c12", fg="#ecf0f1")
        complete_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.task_listbox.bind('<Double-Button-1>', lambda event: self.complete_task())

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            cursor.execute("INSERT INTO tasks (user_id, task, status) VALUES (%s, %s, %s)", (self.user_id, task, "pending"))
            db.commit()
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            cursor.execute("DELETE FROM tasks WHERE user_id = %s AND task = %s", (self.user_id, task))
            db.commit()
            self.tasks.pop(selected_task_index[0])
            self.update_task_list()

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            cursor.execute("UPDATE tasks SET status = %s WHERE user_id = %s AND task = %s", ("completed", self.user_id, task))
            db.commit()
            self.update_task_list()

    def load_tasks(self):
        cursor.execute("SELECT task FROM tasks WHERE user_id = %s AND status = %s", (self.user_id, "pending"))
        self.tasks = [task[0] for task in cursor.fetchall()]
        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
