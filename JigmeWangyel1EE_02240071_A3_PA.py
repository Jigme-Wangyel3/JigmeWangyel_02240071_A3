import tkinter as tk
from tkinter import simpledialog, messagebox


class BankError(Exception):
    """Base exception for banking errors."""
    pass

class InvalidInputError(BankError):
    """Raised when user provides invalid input."""
    pass

class InvalidTransferError(BankError):
    """Raised when a transfer is invalid (e.g. insufficient funds)."""
    pass


class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidInputError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidInputError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InvalidInputError("Insufficient funds.")
        self.balance -= amount

    def __str__(self):
        return f"Account({self.owner}, Balance: {self.balance:.2f})"

class MobileTopUpService:
    def __init__(self):
        self.top_ups = {}  # phone -> total amount

    def top_up(self, phone_number, amount):

        if amount <= 0:
            raise InvalidInputError("Top-up amount must be positive.")
        self.top_ups[phone_number] = self.top_ups.get(phone_number, 0) + amount

    def get_total(self, phone_number):

        return self.top_ups.get(phone_number, 0)

class Bank:

    def __init__(self):
        self.accounts = {}
        self.top_up_service = MobileTopUpService()

    def create_account(self, name, initial_deposit=0):
        if name in self.accounts:
            raise InvalidInputError("Account already exists.")
        acct = Account(name, initial_deposit)
        self.accounts[name] = acct
        return acct

    def get_account(self, name):
        try:
            return self.accounts[name]
        except KeyError:
            raise InvalidInputError("Account not found.")

    def transfer(self, src_name, dest_name, amount):
        if amount <= 0:
            raise InvalidTransferError("Transfer amount must be positive.")
        src = self.get_account(src_name)
        dest = self.get_account(dest_name)
        if src.balance < amount:
            raise InvalidTransferError("Insufficient funds for transfer.")
        src.withdraw(amount)
        dest.deposit(amount)

    def top_up_mobile(self, account_name, phone, amount):
        acct = self.get_account(account_name)
        acct.withdraw(amount)
        self.top_up_service.top_up(phone, amount)

# -------------------- CLI Menu System --------------------

def process_user_input(choice, bank):
    if choice == "1":
        name = input("Name: ")
        deposit = float(input("Initial deposit: "))
        bank.create_account(name, deposit)
        print("Account created.")
    elif choice == "2":
        name = input("Name: ")
        acct = bank.get_account(name)
        print(acct)
    elif choice == "3":
        src = input("From account: ")
        dst = input("To account: ")
        amt = float(input("Amount: "))
        bank.transfer(src, dst, amt)
        print("Transfer complete.")
    elif choice == "4":
        name = input("Account: ")
        phone = input("Phone number: ")
        amt = float(input("Top-up amount: "))
        bank.top_up_mobile(name, phone, amt)
        print("Mobile topped up.")
    elif choice == "5":
        print("Goodbye!")
        return False
    else:
        raise InvalidInputError("Invalid menu choice.")
    return True

def run_cli():
    bank = Bank()
    running = True
    while running:
        print("\n1) Create account\n2) Show account\n3) Transfer funds\n4) Mobile top-up\n5) Quit")
        choice = input("Choice: ")
        try:
            running = process_user_input(choice, bank)
        except BankError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


class BankingGUI:
    def __init__(self, root):
        self.bank = Bank()
        self.root = root
        root.title("Banking App")

        tk.Button(root, text="Create Account", command=self.create_account).pack(fill='x')
        tk.Button(root, text="Show Account", command=self.show_account).pack(fill='x')
        tk.Button(root, text="Transfer Funds", command=self.transfer_funds).pack(fill='x')
        tk.Button(root, text="Mobile Top-up", command=self.mobile_topup).pack(fill='x')
        tk.Button(root, text="Quit", command=root.quit).pack(fill='x')

    def create_account(self):
        try:
            name = simpledialog.askstring("Name", "Account holder name?")
            init = float(simpledialog.askstring("Deposit", "Initial deposit?"))
            self.bank.create_account(name, init)
            messagebox.showinfo("Success", f"Account for {name} created.")
        except (BankError, TypeError, ValueError) as e:
            messagebox.showerror("Error", str(e))

    def show_account(self):
        try:
            name = simpledialog.askstring("Name", "Account name?")
            acct = self.bank.get_account(name)
            messagebox.showinfo("Account Info", str(acct))
        except BankError as e:
            messagebox.showerror("Error", str(e))

    def transfer_funds(self):
        try:
            src = simpledialog.askstring("From", "From account?")
            dst = simpledialog.askstring("To", "To account?")
            amt = float(simpledialog.askstring("Amount", "Amount?"))
            self.bank.transfer(src, dst, amt)
            messagebox.showinfo("Success", "Transfer complete.")
        except (BankError, TypeError, ValueError) as e:
            messagebox.showerror("Error", str(e))

    def mobile_topup(self):
        try:
            name = simpledialog.askstring("Name", "Account name?")
            phone = simpledialog.askstring("Phone", "Phone number?")
            amt = float(simpledialog.askstring("Amount", "Top-up amount?"))
            self.bank.top_up_mobile(name, phone, amt)
            messagebox.showinfo("Success", "Mobile topped up.")
        except (BankError, TypeError, ValueError) as e:
            messagebox.showerror("Error", str(e))

def run_gui():
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    print("Choose mode:")
    print("1) Command-line")
    print("2) GUI")
    mode = input("Enter 1 or 2: ")
    if mode == "1":
        run_cli()
    elif mode == "2":
        run_gui()
    else:
        print("Invalid mode selected.")
