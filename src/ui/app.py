import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import platform

from utils import validate_amount
from models import Transaction, FinanceTracker, TransactionType
from data import Data

class App:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.root.resizable(False, False)
        self.root.title("💰 MoneyLog")
        self.root.geometry("850x820")
        self.root.configure(bg="#f4f4f4")
        self.tracker: FinanceTracker = FinanceTracker()
        self.data: Data = Data()

        self.setup_ui()

        for transaction in self.data.load_transactions():
            self.add_transaction(transaction)

    def quit_me(self):
        self.root.quit()
        self.root.destroy()

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
        self.type_var = tk.StringVar(value="Expense")
        tk.Radiobutton(form_frame, text="Income", variable=self.type_var, value="Income", bg="white").grid(row=2, column=1, sticky="w", pady=3)
        tk.Radiobutton(form_frame, text="Expense", variable=self.type_var, value="Expense", bg="white").grid(row=2, column=1, sticky="e", pady=3)

        self._form_input(form_frame, "Sub-Category:", 3)
        self.subc_entry = ttk.Entry(form_frame)
        self.subc_entry.grid(row=3, column=1, pady=3, padx=5)

        self._form_input(form_frame, "Date (YYYY-MM-DD):", 4)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.grid(row=4, column=1, pady=3, padx=5)

        ttk.Button(form_frame, text="➕ Add Transaction", style="TButton", command=self.add_transaction).grid(row=5, column=0, columnspan=2, pady=10)

        # --- Summary ---
        self.summary_frame = tk.Frame(self.root, bg="#f4f4f4", pady=5)
        self.summary_frame.pack(fill="x")

        self.update_summary()

        # --- Transactions list ---
        list_frame = tk.LabelFrame(self.root, text="🧾 Transactions", padx=10, pady=10, bg="white", font=("Comic Sans MS", 10, "bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        self.transaction_list = tk.Listbox(list_frame, height=18, font=("Comic Sans MS", 10))
        self.transaction_list.pack(fill="both", expand=True)

        # Canvas y scrollbar
        self.canvas = tk.Canvas(self.transaction_list)
        self.scrollbar = ttk.Scrollbar(self.transaction_list, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.bind_mousewheel(list_frame, self.canvas)
        
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
            tk.Label(self.scrollable_frame, text=h, font=("Comic Sans MS", 10, "bold"), borderwidth=2, relief="groove", width=15, bg="lightgray").grid(row=0, column=col, sticky="nsew")

        # --- Charts Button ---
        chart_frame = tk.Frame(self.root, bg="#f4f4f4")
        chart_frame.pack(pady=10)

        ttk.Button(chart_frame, text="📊 Show Charts", style="TButton", command=self.show_charts).pack()

    def _form_input(self, parent, text, row):
        label = tk.Label(parent, text=text, bg="white", font=("Comic Sans MS", 10, "bold"))
        label.grid(row=row, column=0, sticky="w", pady=3)

    def bind_mousewheel(self, widget, target_canvas):

        system = platform.system()

        if system == 'Windows':
            widget.bind_all("<MouseWheel>", lambda event: target_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        elif system == 'Darwin':  # macOS 
            widget.bind_all("<MouseWheel>", lambda event: target_canvas.yview_scroll(int(-1 * (event.delta)), "units"))
        else:  # Linux
            widget.bind_all("<Button-4>", lambda event: target_canvas.yview_scroll(-1, "units"))
            widget.bind_all("<Button-5>", lambda event: target_canvas.yview_scroll(1, "units"))


    def update_summary(self):

        if self.summary_frame:
            for child in self.summary_frame.winfo_children():
                child.destroy()

        self.income_label = ttk.Label(self.summary_frame, text=f"Income: ${self.tracker.total_incone}", style="Header.TLabel")
        self.income_label.pack(side="left", padx=20)

        self.expense_label = ttk.Label(self.summary_frame, text=f"Expenses: ${self.tracker.total_expenses}", style="Header.TLabel")
        self.expense_label.pack(side="left", padx=20)

        self.balance_label = ttk.Label(self.summary_frame, text=f"Balance: ${self.tracker.total_incone - self.tracker.total_expenses}", style="Header.TLabel")
        self.balance_label.pack(side="right", padx=20)

    def add_transaction(self, transaction: Transaction = None):

        if not transaction:
            amount = self.amount_entry.get()
            category = self.category_entry.get()
            type = self.type_var.get()
            subc = self.subc_entry.get()
            date = self.date_entry.get()

            if amount == "" or category == "" or date == "" or subc == "":
                messagebox.showerror("Empty fields", "Amount, date, category and subcategory, have to be non-empty.")
                return
            
            amount = float(amount)

            transaction = Transaction(amount, category, TransactionType(type), date, subc)


        self.tracker.add_transaction(transaction)
        self.data.save_transactions(self.tracker.transactions)

        # Colors
        bg_color: str
        if transaction.type == TransactionType.INCOME:
            bg_color = "#66ff66"
            self.tracker.total_incone += float(transaction.amount)
        else: 
            bg_color = "#FF6666"
            self.tracker.total_expenses += float(transaction.amount)

        self.update_summary()
    
        row = len(self.scrollable_frame.winfo_children()) - 1

        date_frame = tk.Label(self.scrollable_frame, text=transaction.date, borderwidth=1, relief="solid", width=12, bg=bg_color, font=("Comic Sans MS", 9, "bold"))
        date_frame.grid(row=row+1, column=0, sticky="nsew")

        category_frame = tk.Label(self.scrollable_frame, text=transaction.category, borderwidth=1, relief="solid", width=15, bg=bg_color, font=("Comic Sans MS", 9, "bold"))
        category_frame.grid(row=row+1, column=1, sticky="nsew")

        subc_frame = tk.Label(self.scrollable_frame, text=transaction.subcat, borderwidth=1, relief="solid", width=15, bg=bg_color, font=("Comic Sans MS", 9, "bold"))
        subc_frame.grid(row=row+1, column=2, sticky="nsew")

        type_frame = tk.Label(self.scrollable_frame, text=transaction.type.value, borderwidth=1, relief="solid", width=10, bg=bg_color, font=("Comic Sans MS", 9, "bold"))
        type_frame.grid(row=row+1, column=3, sticky="nsew")

        amount_frame = tk.Label(self.scrollable_frame, text=f"${transaction.amount}", borderwidth=1, relief="solid", width=10, bg=bg_color, font=("Comic Sans MS", 9, "bold"))
        amount_frame.grid(row=row+1, column=4, sticky="nsew")

        frames = [date_frame, category_frame, subc_frame, type_frame, amount_frame]

        delete_button = ttk.Button(self.scrollable_frame, text="🗑 Delete", command=lambda: self.delete_transaction(transaction, frames, delete_button), style="TButton")
        delete_button.grid(row=row+1, column=5, sticky="nsew")



    def delete_transaction(self, transaction: Transaction, frames: list[tk.Frame], button: ttk.Button):

        # Delete the transaction from the list
        self.tracker.delete_transaction(transaction)

        if transaction.type == TransactionType.INCOME:
            self.tracker.total_incone -= transaction.amount
        else: 
            self.tracker.total_expenses -= transaction.amount
        self.update_summary()

        for frame in frames:
            frame.destroy()

        button.destroy()

        self.data.save_transactions(self.tracker.transactions)

    def show_charts(self):
        # Create window
        chart_window = tk.Toplevel(self.root)
        chart_window.resizable(False, False)
        chart_window.title("📊 Expense Charts")
        chart_window.geometry("1400x500")  # Más ancho para 3 gráficos
        chart_window.configure(bg="white")

        # Agrupaciones
        category_totals = defaultdict(float)
        subcategory_totals = defaultdict(float)
        total_income = 0
        total_expense = 0

        for t in self.tracker.transactions:
            amount = float(t.amount)
            if t.type == TransactionType.EXPENSE:
                category_totals[t.category] += amount
                subcategory_totals[t.subcat] += amount
                total_expense += amount
            elif t.type == TransactionType.INCOME:
                total_income += amount

        # Create matplotlib figure con 3 gráficos en fila
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
        fig.tight_layout(pad=5.0)

        # --- Gráfico 1: Barras por categoría ---
        if category_totals:
            categories = list(category_totals.keys())
            totals = list(category_totals.values())

            ax1.bar(categories, totals, color="#FF6666")
            ax1.set_title("Expenses by Category")
            ax1.set_ylabel("Amount ($)")
            ax1.set_xlabel("Category")
            ax1.tick_params(axis='x', rotation=45)
        else:
            ax1.text(0.5, 0.5, "No expenses yet", ha="center", va="center", fontsize=12)
            ax1.axis("off")

        # --- Gráfico 2: Pie de ingresos vs egresos ---
        if total_income > 0 or total_expense > 0:
            labels = ['Income', 'Expenses']
            values = [total_income, total_expense]
            colors = ['#66ff66', '#FF6666']
            ax2.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax2.set_title("Income vs Expenses")
        else:
            ax2.text(0.5, 0.5, "No data yet", ha="center", va="center", fontsize=12)
            ax2.axis("off")

        # --- Gráfico 3: Barras por subcategoría ---
        if subcategory_totals:
            subcategories = list(subcategory_totals.keys())
            sub_totals = list(subcategory_totals.values())

            ax3.bar(subcategories, sub_totals, color="#FF9999")
            ax3.set_title("Expenses by Subcategory")
            ax3.set_ylabel("Amount ($)")
            ax3.set_xlabel("Subcategory")
            ax3.tick_params(axis='x', rotation=45)
        else:
            ax3.text(0.5, 0.5, "No subcategories yet", ha="center", va="center", fontsize=12)
            ax3.axis("off")

        # Integración con tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)




