import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL)
""")
conn.commit()


def add_students():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if name == "" or age == "" or course == "":
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?,?,?)",
        (name, age, course)
    )
    conn.commit()
    messagebox.showinfo("Success", "Student added successfully.")
    
    clear_fields()
    display_students()


def display_students():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for idx, student in enumerate(students):
        if idx % 2 == 0:
            tree.insert("", tk.END, values=student, tags=("evenrow",))
        else:
            tree.insert("", tk.END, values=student, tags=("oddrow",))


def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student to update.")
        return

    student_id = tree.item(selected)["values"][0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if name == "" or age == "" or course == "":
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (name, age, course, student_id))
    
    conn.commit()
    messagebox.showinfo("Success", "Student updated successfully.")
    
    clear_fields()
    display_students()


def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student to delete.")
        return

    student_id = tree.item(selected)["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")
            conn.commit()

        messagebox.showinfo("Success", "Student deleted successfully.")
        
        clear_fields()
        display_students()


def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


def select_student(event):
    selected = tree.selection()
    if selected:
        student = tree.item(selected)["values"]
        clear_fields()
        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])


# --- Autumn Leaf Color Scheme Palette Variables ---
BG_COLOR = "#fbfaf7"          # Warm off-white canvas background
TEXT_DARK = "#2b221a"         # Earthy near-black text for high readability
LEAF_GREEN = "#3d4a14"        # Deep Olive Green (Add Button)
LEAF_ORANGE = "#e67e15"       # Warm Orange (Update Button)
LEAF_BROWN = "#4a1c0d"        # Dark Chestnut Brown (Table Headers)
LEAF_TERRACOTTA = "#d95d39"   # Burnt Terracotta (Clear Button)
LEAF_RED_ORANGE = "#df3e2c"   # Brighter Crimson Salmon (Delete Button)
BTN_TEXT_LIGHT = "#ffffff"    # Pure white button text label

root = tk.Tk()
root.title("Student Management System")
root.geometry("600x520")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("clam")

# Custom Table Design Styling
style.configure("Treeview", 
                background="#ffffff", 
                foreground=TEXT_DARK, 
                rowheight=25, 
                fieldbackground="#ffffff")

style.configure("Treeview.Heading", 
                background=LEAF_BROWN, 
                foreground=BTN_TEXT_LIGHT, 
                font=("Arial", 10, "bold"))

style.map("Treeview.Heading", 
          background=[("active", "#361409")])

style.map("Treeview", 
          background=[("selected", LEAF_ORANGE)],
          foreground=[("selected", BTN_TEXT_LIGHT)])

form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(pady=15)

tk.Label(form_frame, text="Name:", bg=BG_COLOR, fg=TEXT_DARK, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#ffffff", fg=TEXT_DARK, relief="solid", bd=1)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Age:", bg=BG_COLOR, fg=TEXT_DARK, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
age_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#ffffff", fg=TEXT_DARK, relief="solid", bd=1)
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Course:", bg=BG_COLOR, fg=TEXT_DARK, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
course_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#ffffff", fg=TEXT_DARK, relief="solid", bd=1)
course_entry.grid(row=2, column=1, padx=5, pady=5)

btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

# Colors mapped explicitly to the visual layout elements from your palette
tk.Button(btn_frame, text="Add", command=add_students, width=10, bg=LEAF_GREEN, fg=BTN_TEXT_LIGHT, activebackground="#2c360e", activeforeground=BTN_TEXT_LIGHT, bd=0, font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_student, width=10, bg=LEAF_ORANGE, fg=BTN_TEXT_LIGHT, activebackground="#cd6f10", activeforeground=BTN_TEXT_LIGHT, bd=0, font=("Arial", 9, "bold")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_student, width=10, bg=LEAF_RED_ORANGE, fg=BTN_TEXT_LIGHT, activebackground="#c63322", activeforeground=BTN_TEXT_LIGHT, bd=0, font=("Arial", 9, "bold")).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_fields, width=10, bg=LEAF_TERRACOTTA, fg=BTN_TEXT_LIGHT, activebackground="#c44e2c", activeforeground=BTN_TEXT_LIGHT, bd=0, font=("Arial", 9, "bold")).grid(row=0, column=3, padx=5)

tree_frame = tk.Frame(root, bg=BG_COLOR)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=15)

columns = ("ID", "Name", "Age", "Course")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)

# Clean, subtle alternating rows
tree.tag_configure("evenrow", background="#ffffff")
tree.tag_configure("oddrow", background="#f8f6f0")

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind("<<TreeviewSelect>>", select_student)

display_students()

root.mainloop()

conn.close()
