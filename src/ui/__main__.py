import tkinter as tk
from tkinter import ttk
from datetime import date

from utils import validate_amount

class App:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("💰 MoneyLog")
        self.root.geometry("640x820")
        self.root.configure(bg="#f4f4f4")

        self.setup_ui()

    def setup_ui(self):
        # --- General styling ---
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="black", font=("Comic Sans MS", 10, "bold"))
        style.configure("TLabel", background="#f4f4f4", font=("Comic Sans MS", 10))
        style.configure("Header.TLabel", font=("Comic Sans MS", 12, "bold"))
        style.configure("TEntry", padding=4, font=("Comic Sans MS", 8, "bold"))

        # --- Main title ---
        tk.Label(self.root, text="💰 MoneyLog", bg="#f4f4f4", font=("Comic Sans MS", 20, "bold")).pack(pady=10)

        # --- Form ---
        form_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid", padx=15, pady=10)
        form_frame.pack(padx=20, pady=5, fill="x")

        self._form_input(form_frame, "Amount:", 0)
        vcmd = (self.root.register(validate_amount), "%P")
        self.amount_entry = ttk.Entry(form_frame, validate="key", validatecommand=vcmd, style="TEntry")
        self.amount_entry.grid(row=0, column=1, pady=3, padx=5)

        self._form_input(form_frame, "Category:", 1)
        self.category_entry = ttk.Entry(form_frame, style="TEntry")
        self.category_entry.grid(row=1, column=1, pady=3, padx=5)

        self._form_input(form_frame, "Type:", 2)
        self.type_var = tk.StringVar(value="expense")
        tk.Radiobutton(form_frame, text="Income", variable=self.type_var, value="income", bg="white").grid(row=2, column=1, sticky="w", pady=3)
        tk.Radiobutton(form_frame, text="Expense", variable=self.type_var, value="expense", bg="white").grid(row=2, column=1, sticky="e", pady=3)

        self._form_input(form_frame, "Description:", 3)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=3, column=1, pady=3, padx=5)

        self._form_input(form_frame, "Date (YYYY-MM-DD):", 4)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.grid(row=4, column=1, pady=3, padx=5)

        ttk.Button(form_frame, text="➕ Add Transaction", style="TButton", command=self.add_transaction).grid(row=5, column=0, columnspan=2, pady=10)

        # --- Summary ---
        summary_frame = tk.Frame(self.root, bg="#f4f4f4", pady=5)
        summary_frame.pack(fill="x")

        self.income_label = ttk.Label(summary_frame, text="Income: $0", style="Header.TLabel")
        self.income_label.pack(side="left", padx=20)

        self.expense_label = ttk.Label(summary_frame, text="Expenses: $0", style="Header.TLabel")
        self.expense_label.pack(side="left", padx=20)

        self.balance_label = ttk.Label(summary_frame, text="Balance: $0", style="Header.TLabel")
        self.balance_label.pack(side="right", padx=20)

        # --- Transactions list ---
        list_frame = tk.LabelFrame(self.root, text="🧾 Transactions", padx=10, pady=10, bg="white", font=("Comic Sans MS", 10, "bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        self.transaction_list = tk.Listbox(list_frame, height=18, font=("Comic Sans MS", 10))
        self.transaction_list.pack(fill="both", expand=True)

        # --- Charts Button ---
        chart_frame = tk.Frame(self.root, bg="#f4f4f4")
        chart_frame.pack(pady=10)

        ttk.Button(chart_frame, text="📊 Show Charts", style="TButton").pack()

    def _form_input(self, parent, text, row):
        label = tk.Label(parent, text=text, bg="white", font=("Comic Sans MS", 10, "bold"))
        label.grid(row=row, column=0, sticky="w", pady=3)

    def add_transaction(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        type = self.type_var.get()
        desc = self.desc_entry.get()
        date = self.date_entry.get()

        print(f"Amount: {amount}, Category: {category}, Type: {type}, Desc: {desc}, Date: {date}")
        # Lógica para validar, guardar, actualizar lista, etc.


# Execute app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
