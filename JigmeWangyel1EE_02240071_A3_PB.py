import unittest
from JigmeWangyel1EE_02240071_A3_PA import Account, Bank, InvalidInputError, InvalidTransferError

class TestBankingApp(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()
        self.bank.create_account("Alice", 100)
        self.bank.create_account("Bob", 50)

    def test_deposit_valid(self):
        acct = self.bank.get_account("Alice")
        acct.deposit(50)
        self.assertEqual(acct.balance, 150)

    def test_deposit_negative(self):
        acct = self.bank.get_account("Alice")
        with self.assertRaises(InvalidInputError):
            acct.deposit(-10)

    def test_withdraw_valid(self):
        acct = self.bank.get_account("Alice")
        acct.withdraw(50)
        self.assertEqual(acct.balance, 50)

    def test_withdraw_insufficient_funds(self):
        acct = self.bank.get_account("Bob")
        with self.assertRaises(InvalidInputError):
            acct.withdraw(100)

    def test_transfer_valid(self):
        self.bank.transfer("Alice", "Bob", 40)
        self.assertEqual(self.bank.get_account("Alice").balance, 60)
        self.assertEqual(self.bank.get_account("Bob").balance, 90)

    def test_transfer_invalid_amount(self):
        with self.assertRaises(InvalidTransferError):
            self.bank.transfer("Alice", "Bob", -20)

    def test_transfer_insufficient(self):
        with self.assertRaises(InvalidTransferError):
            self.bank.transfer("Bob", "Alice", 100)

    def test_transfer_nonexistent_account(self):
        with self.assertRaises(InvalidInputError):
            self.bank.transfer("Alice", "Charlie", 10)

    def test_mobile_topup_valid(self):
        self.bank.top_up_mobile("Alice", "1234567890", 30)
        self.assertEqual(self.bank.top_up_service.get_total("1234567890"), 30)
        self.assertEqual(self.bank.get_account("Alice").balance, 70)

    def test_mobile_topup_insufficient(self):
        with self.assertRaises(InvalidInputError):
            self.bank.top_up_mobile("Bob", "999", 999)

    def test_create_duplicate_account(self):
        with self.assertRaises(InvalidInputError):
            self.bank.create_account("Alice", 10)

    def test_create_account_negative_balance(self):
        with self.assertRaises(InvalidInputError):
            self.bank.create_account("Evil", -100)

    def test_get_nonexistent_account(self):
        with self.assertRaises(InvalidInputError):
            self.bank.get_account("Ghost")

    def test_delete_account_manual(self):
        del self.bank.accounts["Alice"]
        self.assertNotIn("Alice", self.bank.accounts)

if __name__ == '__main__':
    unittest.main()
