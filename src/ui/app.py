import tkinter as tk
from tkinter import ttk
from datetime import date

from utils import validate_amount
from models import Transaction, Data, FinanceTracker

class App:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("💰 MoneyLog")
        self.root.geometry("840x820")
        self.root.configure(bg="#f4f4f4")
        self.tracker: FinanceTracker = FinanceTracker()
        self.data: Data = Data()

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
        form_frame.pack(padx=20, pady=5, fill="y")

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

        self._form_input(form_frame, "Sub-Category:", 3)
        self.subc_entry = ttk.Entry(form_frame)
        self.subc_entry.grid(row=3, column=1, pady=3, padx=5)

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

        # Canvas y scrollbar
        self.canvas = tk.Canvas(self.transaction_list)
        self.scrollbar = ttk.Scrollbar(self.transaction_list, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configurar scroll en el canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        headers = ["Date", "Category", "Sub-Category", "Type", "Amount", "Action"]
        for col, h in enumerate(headers):
            tk.Label(self.scrollable_frame, text=h, font=("Arial", 10, "bold"), borderwidth=2, relief="groove", width=15, bg="lightgray").grid(row=0, column=col, sticky="nsew")

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
        subc = self.subc_entry.get()
        date = self.date_entry.get()

        transaction = Transaction(amount, category, type, date, subc)
        self.tracker.add_transaction(transaction)

        # Colors
        bg_color = "#66ff66" if transaction.type == "income" else "#FF6666"

        row = len(self.scrollable_frame.winfo_children()) - 1  # -1 porque headers ocupa la primera fila

        date_frame = tk.Label(self.scrollable_frame, text=date, borderwidth=1, relief="solid", width=12, bg=bg_color)
        date_frame.grid(row=row+1, column=0, sticky="nsew")
        category_frame = tk.Label(self.scrollable_frame, text=category, borderwidth=1, relief="solid", width=15, bg=bg_color)
        category_frame.grid(row=row+1, column=1, sticky="nsew")
        subc_frame = tk.Label(self.scrollable_frame, text=subc, borderwidth=1, relief="solid", width=15, bg=bg_color)
        subc_frame.grid(row=row+1, column=2, sticky="nsew")
        type_frame = tk.Label(self.scrollable_frame, text=type.capitalize(), borderwidth=1, relief="solid", width=10, bg=bg_color)
        type_frame.grid(row=row+1, column=3, sticky="nsew")
        amount_frame = tk.Label(self.scrollable_frame, text=f"${amount}", borderwidth=1, relief="solid", width=10, bg=bg_color)
        amount_frame.grid(row=row+1, column=4, sticky="nsew")

        frames = [date_frame, category_frame, subc_frame, type_frame, amount_frame]

        delete_button = ttk.Button(self.scrollable_frame, text="🗑 Delete", command=lambda: self.delete_transaction(transaction, frames, delete_button))
        delete_button.grid(row=row+1, column=5, sticky="nsew")


    def delete_transaction(self, transaction: Transaction, frames: list[tk.Frame], button: ttk.Button):

        # Delete the transaction from the list
        self.tracker.delete_transaction(transaction)

        for frame in frames:
            frame.destroy()

        button.destroy()


