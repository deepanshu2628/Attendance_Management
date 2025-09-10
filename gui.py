import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # pyright: ignore[reportMissingImports]
from database import add_student, update_student, delete_student, get_students, mark_attendance, get_attendance
from export import export_attendance
from datetime import date

def launch_gui():
    root = tk.Tk()
    root.title("Attendance Management System - Upgraded")
    root.geometry("900x600")
    root.configure(bg="#f0f0f0")

    tab_control = ttk.Notebook(root)
    
    student_tab = ttk.Frame(tab_control)
    tab_control.add(student_tab, text='Students')
    
    attendance_tab = ttk.Frame(tab_control)
    tab_control.add(attendance_tab, text='Attendance')
    
    tab_control.pack(expand=1, fill='both')

    # --- Student Tab ---
    tk.Label(student_tab, text="Name").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(student_tab, text="Roll No").grid(row=1, column=0, padx=5, pady=5)
    name_entry = tk.Entry(student_tab)
    roll_entry = tk.Entry(student_tab)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    roll_entry.grid(row=1, column=1, padx=5, pady=5)

    search_entry = tk.Entry(student_tab)
    search_entry.grid(row=0, column=3, padx=5, pady=5)
    tk.Label(student_tab, text="Search").grid(row=0, column=2, padx=5, pady=5)

    student_tree = ttk.Treeview(student_tab, columns=("ID", "Name", "Roll"), show='headings')
    student_tree.heading("ID", text="ID")
    student_tree.heading("Name", text="Name")
    student_tree.heading("Roll", text="Roll No")
    student_tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    def show_students():
        for row in student_tree.get_children():
            student_tree.delete(row)
        search = search_entry.get()
        for student in get_students(search):
            student_tree.insert("", tk.END, values=student)

    def add_student_gui():
        name = name_entry.get()
        roll = roll_entry.get()
        if name and roll:
            add_student(name, roll)
            messagebox.showinfo("Success", "Student added!")
            name_entry.delete(0, tk.END)
            roll_entry.delete(0, tk.END)
            show_students()
        else:
            messagebox.showerror("Error", "Enter all fields!")

    def update_student_gui():
        selected = student_tree.selection()
        if selected:
            student_id = student_tree.item(selected[0])['values'][0]
            update_student(student_id, name_entry.get(), roll_entry.get())
            messagebox.showinfo("Success", "Student updated!")
            show_students()
        else:
            messagebox.showerror("Error", "Select a student!")

    def delete_student_gui():
        selected = student_tree.selection()
        if selected:
            student_id = student_tree.item(selected[0])['values'][0]
            delete_student(student_id)
            messagebox.showinfo("Success", "Student deleted!")
            show_students()
        else:
            messagebox.showerror("Error", "Select a student!")

    tk.Button(student_tab, text="Add", command=add_student_gui, bg="#4CAF50", fg="white").grid(row=2, column=0, pady=5)
    tk.Button(student_tab, text="Update", command=update_student_gui, bg="#2196F3", fg="white").grid(row=2, column=1, pady=5)
    tk.Button(student_tab, text="Delete", command=delete_student_gui, bg="#f44336", fg="white").grid(row=2, column=2, pady=5)
    tk.Button(student_tab, text="Search", command=show_students).grid(row=0, column=4, padx=5)
    show_students()

    # --- Attendance Tab ---
    student_att_tree = ttk.Treeview(attendance_tab, columns=("Roll", "Name", "Date", "Status"), show='headings')
    student_att_tree.heading("Roll", text="Roll No")
    student_att_tree.heading("Name", text="Name")
    student_att_tree.heading("Date", text="Date")
    student_att_tree.heading("Status", text="Status")
    student_att_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    date_entry = DateEntry(attendance_tab, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=0, column=0, padx=5, pady=5)

    def show_attendance():
        for row in student_att_tree.get_children():
            student_att_tree.delete(row)
        search = search_entry.get()
        for att in get_attendance(search):
            student_att_tree.insert("", tk.END, values=att)

    def mark_present():
        selected = student_tree.selection()
        if selected:
            student_id = student_tree.item(selected[0])['values'][0]
            mark_attendance(student_id, str(date_entry.get_date()), "Present")
            show_attendance()

    def mark_absent():
        selected = student_tree.selection()
        if selected:
            student_id = student_tree.item(selected[0])['values'][0]
            mark_attendance(student_id, str(date_entry.get_date()), "Absent")
            show_attendance()

    tk.Button(attendance_tab, text="Mark Present", command=mark_present, bg="#4CAF50", fg="white").grid(row=0, column=1)
    tk.Button(attendance_tab, text="Mark Absent", command=mark_absent, bg="#f44336", fg="white").grid(row=0, column=2)
    tk.Button(attendance_tab, text="Export Attendance", command=lambda: export_attendance(), bg="#FF9800", fg="white").grid(row=0, column=3)

    show_attendance()

    root.mainloop()
