import hashlib
import json
import random
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# ==========================================
# BACKEND LOGIC (The "Engine")
# ==========================================

class BankAccount:
    def __init__(self, name, balance, pin, account_number=None, history=None, is_hashed=False):
        self.name = name
        self.balance = balance
        self.account_number = account_number if account_number else random.randint(10000, 99999)
        self.history = history if history else [f"Account created with ${balance}"]

        if is_hashed:
            self.pin_hash = pin
        else:
            self.pin_hash = self._hash_pin(pin)

    def _hash_pin(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    def check_pin(self, input_pin):
        return self.pin_hash == self._hash_pin(input_pin)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(f"Deposited ${amount}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append(f"Withdrew ${amount}")
            return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "pin": self.pin_hash,
            "account_number": self.account_number,
            "history": self.history
        }

class Bank:
    def __init__(self, filename='bank_vault.json'):
        self.filename = filename
        self.accounts = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    for acc_num, info in data.items():
                        self.accounts[int(acc_num)] = BankAccount(**info, is_hashed=True)
            except Exception as e:
                print(f"Error loading database: {e}")

    def save_data(self):
        with open(self.filename, 'w') as f:
            json_data = {acc_num: acc.to_dict() for acc_num, acc in self.accounts.items()}
            json.dump(json_data, f, indent=4)

    def create_account(self, name, initial_deposit, pin):
        new_acc = BankAccount(name, initial_deposit, pin)
        self.accounts[new_acc.account_number] = new_acc
        self.save_data()
        return new_acc

# ==========================================
# FRONTEND GUI (The "Interface")
# ==========================================

class BankApp:
    def __init__(self, root):
        self.bank = Bank()
        self.root = root
        self.root.title("Python Secure Banking System")
        self.root.geometry("400x550")
        self.root.configure(bg="#f0f0f0")
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="PYTHON CENTRAL BANK", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=30)

        btn_style = {"width": 20, "font": ("Helvetica", 12), "pady": 10}
        tk.Button(self.root, text="Open New Account", command=self.show_create_account, **btn_style, bg="#3498db", fg="white").pack(pady=10)
        tk.Button(self.root, text="Login to Account", command=self.show_login, **btn_style, bg="#2ecc71", fg="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, **btn_style, bg="#e74c3c", fg="white").pack(pady=10)

    def show_create_account(self):
        self.clear_screen()
        tk.Label(self.root, text="Register New Account", font=("Helvetica", 14, "bold")).pack(pady=20)

        tk.Label(self.root, text="Full Name:").pack()
        name_ent = tk.Entry(self.root, font=("Helvetica", 12))
        name_ent.pack(pady=5)

        tk.Label(self.root, text="Initial Deposit ($):").pack()
        dep_ent = tk.Entry(self.root, font=("Helvetica", 12))
        dep_ent.pack(pady=5)

        tk.Label(self.root, text="Set 4-Digit PIN:").pack()
        pin_ent = tk.Entry(self.root, show="*", font=("Helvetica", 12))
        pin_ent.pack(pady=5)

        def submit():
            try:
                name = name_ent.get()
                amt = float(dep_ent.get())
                pin = pin_ent.get()
                if not name or not pin:
                    raise ValueError("All fields required")

                acc = self.bank.create_account(name, amt, pin)
                messagebox.showinfo("Success", f"Account Created!\nNumber: {acc.account_number}\nPlease keep this number safe.")
                self.show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid details and numbers.")

        tk.Button(self.root, text="Create Account", command=submit, bg="#3498db", fg="white").pack(pady=20)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack()

    def show_login(self):
        self.clear_screen()
        tk.Label(self.root, text="Account Login", font=("Helvetica", 14, "bold")).pack(pady=20)

        tk.Label(self.root, text="Account Number:").pack()
        acc_ent = tk.Entry(self.root, font=("Helvetica", 12))
        acc_ent.pack(pady=5)

        tk.Label(self.root, text="Enter PIN:").pack()
        pin_ent = tk.Entry(self.root, show="*", font=("Helvetica", 12))
        pin_ent.pack(pady=5)

        def attempt_login():
            try:
                acc_num = int(acc_ent.get())
                pin = pin_ent.get()
                if acc_num in self.bank.accounts:
                    account = self.bank.accounts[acc_num]
                    if account.check_pin(pin):
                        self.show_dashboard(account)
                    else:
                        messagebox.showerror("Denied", "Incorrect PIN.")
                else:
                    messagebox.showerror("Error", "Account not found.")
            except ValueError:
                messagebox.showerror("Error", "Invalid entry.")

        tk.Button(self.root, text="Login", command=attempt_login, bg="#2ecc71", fg="white", width=15).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack()

    def show_dashboard(self, account):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {account.name}", font=("Helvetica", 16, "bold")).pack(pady=20)

        balance_label = tk.Label(self.root, text=f"Current Balance: ${account.balance}", font=("Helvetica", 14), fg="green")
        balance_label.pack(pady=10)

        def refresh_ui():
            balance_label.config(text=f"Current Balance: ${account.balance}")
            self.bank.save_data()

        def deposit_ui():
            amt = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
            if amt and account.deposit(amt):
                refresh_ui()
                messagebox.showinfo("Success", f"Deposited ${amt}")

        def withdraw_ui():
            amt = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
            if amt:
                if account.withdraw(amt):
                    refresh_ui()
                    messagebox.showinfo("Success", f"Withdrew ${amt}")
                else:
                    messagebox.showerror("Error", "Insufficient funds.")

        def history_ui():
            history_str = "\n".join(account.history[-10:]) # Show last 10
            messagebox.showinfo("Transaction History", history_str)

        btn_style = {"width": 25, "pady": 5}
        tk.Button(self.root, text="Deposit Money", command=deposit_ui, **btn_style).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", command=withdraw_ui, **btn_style).pack(pady=5)
        tk.Button(self.root, text="View History", command=history_ui, **btn_style).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.show_main_menu, bg="#95a5a6", fg="white").pack(pady=20)

# ==========================================
# EXECUTION
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()