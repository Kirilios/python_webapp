import sqlite3
from sql_databases import Database
import tkinter as tk
from tkinter import messagebox

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Справочник сотрудников")
        self.db = Database()
        self.db.initialize_tables()
        self.create_widgets()

    def create_widgets(self):
        # Метки и поля
        labels = [
            "ФИО", "Дата рождения (ГГГГ-ММ-ДД)", "Должность",
            "Телефон", "Email", "ID отдела", "ID руководителя"
        ]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(self.root, text=label_text).grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = tk.Entry(self.root, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label_text] = entry

        # Кнопка GUI Добавить человека
        tk.Button(
            self.root, text="Добавить сотрудника",
            command=self.add_employee, bg="white"
        ).grid(row=len(labels), column=0, columnspan=2, pady=6)

        # Кнопка GUI Показать сотрудников отдела
        tk.Button(
            self.root, text="Показать сотрудников отдела",
            command=self.show_by_department, bg="lightblue"
        ).grid(row=len(labels) + 1, column=0, columnspan=3, pady=6)

        # Кнопка GUI Показать подчинённых
        tk.Button(
            self.root, text="Показать подчинённых руководителя",
            command=self.show_by_manager, bg="lightyellow"
        ).grid(row=len(labels) + 2, column=0, columnspan=2, pady=5)

        # Три кнопки для работы с департаментами
        tk.Label(self.root, text="Новый департамент").grid(row=len(labels)+4, column=0, padx=10, sticky='w')
        self.dept_entry = tk.Entry(self.root, width=40)
        self.dept_entry.grid(row=len(labels)+4, column=1, padx=5, pady=5)

        tk.Button(
            self.root, text="Добавить департамент",
            command=self.add_department, bg="lightgreen"
        ).grid(row=len(labels)+5, column=0, columnspan=2, pady=5)

        tk.Button(
            self.root, text="Показать все департаменты",
            command=self.show_departments, bg="lightgray"
        ).grid(row=len(labels)+6, column=0, columnspan=2, pady=5)

        # Поле вывода результатов
        self.result_text = tk.Text(self.root, height=10, width=60)
        self.result_text.grid(row=len(labels) + 3, column=0, columnspan=2, padx=10, pady=10)

    def add_employee(self):
        try:
            full_name = self.entries["ФИО"].get()
            birth_date = self.entries["Дата рождения (ГГГГ-ММ-ДД)"].get()
            position = self.entries["Должность"].get()
            phone = self.entries["Телефон"].get()
            email = self.entries["Email"].get()
            department_id = self.entries["ID отдела"].get()
            manager_id = self.entries["ID руководителя"].get() or None

            if not full_name or not birth_date or not position:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля.")
                return

            self.db.insert_employee(
                full_name, birth_date, position, phone, email,
                int(department_id) if department_id else None,
                int(manager_id) if manager_id else None
            )

            messagebox.showinfo("Успех", "Сотрудник успешно добавлен.")
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении: {e}")

    def add_department(self):
        name = self.dept_entry.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Введите название департамента.")
            return

        added = self.db.insert_department(name)
        if added:
            messagebox.showinfo("Успех", f"Департамент '{name}' добавлен.")
            self.dept_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Предупреждение", f"Департамент '{name}' уже существует.")

    def show_departments(self):
        self.result_text.delete(1.0, tk.END)
        departments = self.db.get_all_departments()
        if departments:
            self.result_text.insert(tk.END, "Список департаментов:\n\n")
            for dept in departments:
                self.result_text.insert(tk.END, f"ID: {dept[0]} | {dept[1]}\n")
        else:
            self.result_text.insert(tk.END, "Нет добавленных департаментов.")
    def show_by_department(self):
        """Показываем людей в отделе"""
        department_id = self.entries["ID отдела"].get()
        if not department_id:
            messagebox.showwarning("Ошибка", "Введите ID отдела.")
            return

        results = self.db.get_employees_by_department(department_id)
        self.result_text.delete(1.0, tk.END)

        if results:
            self.result_text.insert(tk.END, f"Сотрудники отдела {department_id}:\n\n")
            for emp in results:
                self.result_text.insert(tk.END, f"ID: {emp[0]} | {emp[1]} — {emp[2]}\n")
        else:
            self.result_text.insert(tk.END, "В этом отделе нет сотрудников.\n")

    def show_by_manager(self):
        """Показать людей по менеджеру"""
        manager_id = self.entries["ID руководителя"].get()
        if not manager_id:
            messagebox.showwarning("Ошибка", "Введите ID руководителя.")
            return

        results = self.db.get_subordinates_by_manager(manager_id)
        self.result_text.delete(1.0, tk.END)

        if results:
            self.result_text.insert(tk.END, f"Сотрудники, подчинённые руководителю {manager_id}:\n\n")
            for emp in results:
                self.result_text.insert(tk.END, f"ID: {emp[0]} | {emp[1]} — {emp[2]}\n")
        else:
            self.result_text.insert(tk.END, f"У сотрудника с ID {manager_id} нет подчинённых.\n")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def __del__(self):
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()