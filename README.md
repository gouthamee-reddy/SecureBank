# 🏦 SecureBank — Python Desktop Banking System

A desktop banking application built with Python and Tkinter. Supports account creation, secure PIN-based login, deposits, withdrawals, and transaction history — all with data persistence via JSON.

---

##  Features

- **Create Account** — register with name, initial deposit, and a 4-digit PIN
- **Secure Login** — PIN authenticated using SHA-256 hashing (never stored in plain text)
- **Deposit & Withdraw** — real-time balance updates with validation
- **Transaction History** — view last 10 transactions per account
- **Data Persistence** — account data saved locally using JSON

---

##  Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Language | Python 3                |
| GUI      | Tkinter                 |
| Security | hashlib (SHA-256)       |
| Storage  | JSON                    |
| Concepts | OOP, File I/O           |

---

##  Project Structure

```
SecureBank/
├── banking.py       # Main application (backend + GUI)
└── bank_vault.json  # Auto-generated on first run (local only)
```

---

##  How to Run

**Requirements:** Python 3.x (Tkinter is included by default)

```bash
git clone https://github.com/gouthamee-reddy/SecureBank
cd SecureBank
python banking.py
```

---

##  Architecture

The project follows a clean separation of concerns:

- **`BankAccount` class** — handles individual account logic (hashing, deposit, withdraw)
- **`Bank` class** — manages all accounts, handles JSON load/save
- **`BankApp` class** — Tkinter GUI layer, renders screens and handles user interaction

---

##  Limitations

- Uses JSON instead of a proper database (e.g., SQLite)
- No fund transfer between accounts
- Single-user session at a time
- Basic UI design

---

##  Future Improvements

- Migrate storage to SQLite or PostgreSQL
- Add inter-account fund transfers
- Implement session timeout for security
- Improve UI with a modern framework
