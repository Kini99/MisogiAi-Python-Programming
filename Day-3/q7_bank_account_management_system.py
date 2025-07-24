class Account:
    bank_name = "ABC Bank"
    total_accounts = 0
    minimum_balance = 0

    def __init__(self, account_id, holder_name, balance):
        if not account_id or not holder_name or balance < 0:
            raise ValueError("Invalid account details")
        
        self.account_id = account_id
        self.holder_name = holder_name
        self._balance = balance

        Account.total_accounts += 1

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount):
        if amount > 0 and self._balance - amount >= Account.minimum_balance:
            self._balance -= amount
            return amount
        return 0

    def get_balance(self):
        return self._balance

    @classmethod
    def set_bank_name(cls, name):
        cls.bank_name = name

    @classmethod
    def set_minimum_balance(cls, amount):
        cls.minimum_balance = amount

    @classmethod
    def get_total_accounts(cls):
        return cls.total_accounts

    def __str__(self):
        return f"{self.account_id} - {self.holder_name} (${self._balance})"


class SavingsAccount(Account):
    def __init__(self, account_id, holder_name, balance, interest_rate):
        super().__init__(account_id, holder_name, balance)
        if interest_rate < 0:
            raise ValueError("Interest rate must be non-negative")
        self.interest_rate = interest_rate

    def calculate_monthly_interest(self):
        return round(self._balance * self.interest_rate / 100 / 12, 2)


class CheckingAccount(Account):
    def __init__(self, account_id, holder_name, balance, overdraft_limit):
        super().__init__(account_id, holder_name, balance)
        if overdraft_limit < 0:
            raise ValueError("Overdraft limit must be non-negative")
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and self._balance - amount >= -self.overdraft_limit:
            self._balance -= amount
            return amount
        return 0


# Test Case 1: Creating different types of accounts
savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)

print(f"Savings Account: {savings_account}")
print(f"Checking Account: {checking_account}")

# Test Case 2: Deposit and Withdrawal operations
print(f"Savings balance before: ${savings_account.get_balance()}")
savings_account.deposit(500)
print(f"After depositing $500: ${savings_account.get_balance()}")

withdrawal_result = savings_account.withdraw(200)
print(f"Withdrawal result: {withdrawal_result}")
print(f"Balance after withdrawal: ${savings_account.get_balance()}")

# Test Case 3: Overdraft protection in checking account
print(f"Checking balance: ${checking_account.get_balance()}")
overdraft_result = checking_account.withdraw(600)  # Should use overdraft
print(f"Overdraft withdrawal: {overdraft_result}")
print(f"Balance after overdraft: ${checking_account.get_balance()}")

# Test Case 4: Interest calculation for savings
interest_earned = savings_account.calculate_monthly_interest()
print(f"Monthly interest earned: ${interest_earned}")

# Test Case 5: Class methods and variables
print(f"Total accounts created: {Account.get_total_accounts()}")
print(f"Bank name: {Account.bank_name}")

# Change bank settings using class method
Account.set_bank_name("New National Bank")
Account.set_minimum_balance(100)

# Test Case 6: Account validation
try:
    invalid_account = SavingsAccount("SA002", "", -100, 1.5)  # Should raise error
except ValueError as e:
    print(f"Validation error: {e}")
