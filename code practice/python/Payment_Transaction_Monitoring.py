"""
We are developing a payment transaction monitoring system that tracks accounts
and their transactions. The system can compute each account's current balance
and basic statistics.
 
Definitions:
* An "account" has a unique account_id and an owner name.
* A "transaction" represents money moving in or out of an account.
  - DEPOSIT increases the account balance.
  - WITHDRAWAL decreases the account balance.
* "AccountManager" manages accounts and transactions and provides
  balance-related methods.
 
To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Please take as much time
     as necessary, and feel free to run it.
1-2) The test for AccountManager is not passing due to a bug in the code.
     Make the necessary changes to AccountManager to fix the bug.

Clarifications
	· Each transaction has a positive amount in the input.
	· DEPOSIT transactions increase the account balance.
	· WITHDRAWAL transactions decrease the account balance.
	· Transactions are valid and always reference existing accounts.
	· The order of transactions does not need to be modified for this question.  

"""
"""
We are extending our payment transaction monitoring system to support
basic analytics over transactions.
 
For this task, we want to calculate the average transaction amount per account.
 
2) Implement the function get_average_transaction_amount_by_account in AccountManager that returns
the average transaction amount for each account.
 
Requirements:
- The result should associate each account_id with the average amount of its transactions.
- Both DEPOSIT and WITHDRAWAL transactions should be considered.
- Transaction amounts should be treated as absolute values when calculating averages.
- Accounts with no transactions should not appear in the result.
- Transactions always refer to valid accounts.
 
To assist you in testing this new function, we have provided the
test_get_average_transaction_amount_by_account test.

Clarifications
	· Both DEPOSIT and WITHDRAWAL transactions should be included.
	· Transaction amounts are always positive in the input.
	· When calculating averages, use the absolute transaction amount (ignore sign).
	· Transactions are not guaranteed to be in any specific order for this question.
	· Accounts with zero transactions should be excluded from the result.
Pitfalls
	· Treating WITHDRAWAL transactions as negative values when computing averages.
	· Creating entries for accounts that have no transactions.
	· Dividing by the total number of accounts instead of the number of transactions per account.
	· Returning averages per transaction type instead of per account.
 
"""
"""
We are extending our payment transaction monitoring system to calculate
transaction fees based on business rules.

Each account is charged transaction fees as follows:

- The first 3 transactions for an account are FREE.
- From the 4th transaction onward:
  - DEPOSIT transactions cost a flat fee of $1.
  - WITHDRAWAL transactions cost a flat fee of $2.

Transactions must be processed in chronological order (by timestamp).
Fees are applied per account independently.

3) Implement get_transaction_fees() in AccountManager. The function should
return a dictionary associating each account_id with the total transaction
fees charged to that account.

- An account that has transactions but no chargeable ones must appear in the result with a fee of 0.0.
- An account with no transactions must not appear in the result.

To assist you in testing this new function, we have provided the
test_get_transaction_fees function.

Clarifications
•	The first 3 transactions per account are free.
•	Fees are applied starting from the 4th transaction, per account.
•	Transactions must be processed in timestamp order.
•	DEPOSIT transactions incur a $1 fee after the free threshold.
•	WITHDRAWAL transactions incur a $2 fee after the free threshold.
•	Accounts that have transactions but no chargeable ones should appear with a fee of $0.
•	Accounts with no transactions at all should not appear in the result.
Pitfalls
•	Applying the free transaction threshold globally instead of per account.
•	Ignoring transaction order and charging fees incorrectly.
•	Applying fees to the first three transactions.
•	Mixing up DEPOSIT and WITHDRAWAL fee amounts.
•	Forgetting to include accounts that have transactions but no fees (should return $0, not be omitted).

"""


from enum import Enum
from typing import Dict, List
import unittest


class TransactionType(Enum):
  DEPOSIT = "DEPOSIT"
  WITHDRAWAL = "WITHDRAWAL"


class Account:

  def __init__(self, account_id: int, owner_name: str):
    self.account_id = account_id
    self.owner_name = owner_name


class Transaction:

  def __init__(
      self,
      transaction_id: int,
      account_id: int,
      tx_type: TransactionType,
      amount: float,  # Always positive in inputs
      timestamp_sec: int,  # Unix-style seconds (monotonic for tests)
  ):
    self.transaction_id = transaction_id
    self.account_id = account_id
    self.type = tx_type
    self.amount = amount
    self.timestamp_sec = timestamp_sec


class AccountManager:

  def __init__(self):
    self.accounts: Dict[int, Account] = {}
    self.transactions: List[Transaction] = []

  def add_account(self, account: Account):
    self.accounts[account.account_id] = account

  def add_transaction(self, tx: Transaction):
    self.transactions.append(tx)

  def get_balance(self, account_id: int) -> float:
    balance = 0.0
    for tx in self.transactions:
      if tx.account_id == account_id:
        if tx.type == TransactionType.DEPOSIT:
          balance += tx.amount
        elif tx.type == TransactionType.WITHDRAWAL:
          balance -= tx.amount
    return balance

  # New analytics method
  def get_average_transaction_amount_by_account(self) -> Dict[int, float]:
    totals: Dict[int, float] = {}
    counts: Dict[int, int] = {}

    for tx in self.transactions:
      account_id = tx.account_id
      if account_id not in totals:
        totals[account_id] = 0.0
        counts[account_id] = 0
      totals[account_id] += tx.amount
      counts[account_id] += 1

    averages: Dict[int, float] = {}
    for account_id in totals:
      averages[account_id] = totals[account_id] / counts[account_id]

    return averages


  def get_transaction_fees(self) -> Dict[int, float]:
    fees: Dict[int, float] = {}
    counts: Dict[int, int] = {}

    # 1. Sort transactions chronologically by timestamp
    sorted_txs = sorted(self.transactions, key=lambda tx: tx.timestamp_sec)

    # 2. Process transactions in order
    for tx in sorted_txs:
        account_id = tx.account_id

        # Initialize account if seeing it for the first time
        if account_id not in fees:
            fees[account_id] = 0.0
            counts[account_id] = 0
        # Increment the count on every single transaction
        counts[account_id] += 1

        # Charge fees starting from the 4th transaction
        if counts[account_id] > 3:
            if tx.type == TransactionType.DEPOSIT:
                fees[account_id] += 1.0
            elif tx.type == TransactionType.WITHDRAWAL:
                fees[account_id] += 2.0

    return fees

  def get_suspicious_accounts(self) -> List[int]:
    from collections import defaultdict

    account_withdrawals = defaultdict(list)
    for tx in self.transactions:
      if tx.type == TransactionType.WITHDRAWAL and tx.amount >= 50.0:
        account_withdrawals[tx.account_id].append(tx.timestamp_sec)

    suspicious_set = set()

    for account_id, timestamps in account_withdrawals.items():
      timestamps.sort()
      for i in range(len(timestamps)):
        window_end = timestamps[i] + 60
        count = 0
        for j in range(i, len(timestamps)):
          if timestamps[j] <= window_end:
            count += 1
          else:
            break

        if count >= 3:
          suspicious_set.add(account_id)
          break

    return sorted(list(suspicious_set))
# ---------------- Tests ----------------
class TestSuite(unittest.TestCase):

  def test_get_balance_basic(self):
    print("Running test_get_balance_basic")
    mgr = AccountManager()
    mgr.add_account(Account(1, "Alice"))

    mgr.add_transaction(
        Transaction(101, 1, TransactionType.DEPOSIT, 100.0, 1000)
    )
    mgr.add_transaction(
        Transaction(102, 1, TransactionType.WITHDRAWAL, 30.0, 1010)
    )
    mgr.add_transaction(
        Transaction(103, 1, TransactionType.WITHDRAWAL, 20.0, 1020)
    )
    mgr.add_transaction(
        Transaction(104, 1, TransactionType.DEPOSIT, 10.0, 1030)
    )

    self.assertAlmostEqual(60.0, mgr.get_balance(1), places=4)

    mgr.add_transaction(
        Transaction(105, 1, TransactionType.WITHDRAWAL, 70.0, 1045)
    )
    self.assertAlmostEqual(-10.0, mgr.get_balance(1), places=4)

  def test_get_balance_multiple_accounts(self):
    print("Running test_get_balance_multiple_accounts")
    mgr = AccountManager()
    mgr.add_account(Account(1, "Alice"))
    mgr.add_account(Account(2, "Bob"))

    mgr.add_transaction(
        Transaction(201, 1, TransactionType.DEPOSIT, 50.0, 2000)
    )
    mgr.add_transaction(
        Transaction(202, 2, TransactionType.DEPOSIT, 80.0, 2005)
    )
    mgr.add_transaction(
        Transaction(203, 1, TransactionType.WITHDRAWAL, 10.0, 2010)
    )
    mgr.add_transaction(
        Transaction(204, 2, TransactionType.WITHDRAWAL, 5.5, 2015)
    )
    mgr.add_transaction(
        Transaction(205, 2, TransactionType.WITHDRAWAL, 14.5, 2020)
    )

    self.assertAlmostEqual(40.0, mgr.get_balance(1), places=4)
    self.assertAlmostEqual(60.0, mgr.get_balance(2), places=4)

  # Added the extended test
  def test_get_average_transaction_amount_by_account(self):
    print("Running test_get_average_transaction_amount_by_account")
    mgr = AccountManager()

    mgr.add_account(Account(51, "Alice"))
    mgr.add_account(Account(72, "Bob"))
    mgr.add_account(Account(93, "Charlie"))  # no transactions

    # Account 51: 100, 30, 20, 10 => avg = 160 / 4 = 40
    mgr.add_transaction(
        Transaction(101, 51, TransactionType.DEPOSIT, 100.0, 1000)
    )
    mgr.add_transaction(
        Transaction(102, 51, TransactionType.WITHDRAWAL, 30.0, 1010)
    )
    mgr.add_transaction(
        Transaction(103, 51, TransactionType.WITHDRAWAL, 20.0, 1020)
    )
    mgr.add_transaction(
        Transaction(104, 51, TransactionType.DEPOSIT, 10.0, 1030)
    )

    # Account 72: 80, 5.5, 14.5 => avg = 100 / 3 ≈ 33.3333
    mgr.add_transaction(
        Transaction(201, 72, TransactionType.DEPOSIT, 80.0, 2005)
    )
    mgr.add_transaction(
        Transaction(202, 72, TransactionType.WITHDRAWAL, 5.5, 2015)
    )
    mgr.add_transaction(
        Transaction(203, 72, TransactionType.WITHDRAWAL, 14.5, 2020)
    )

    avg = mgr.get_average_transaction_amount_by_account()

    self.assertAlmostEqual(40.0, avg[51], places=4)
    self.assertAlmostEqual(33.3333, avg[72], places=4)

    # Account 93 has no transactions -> should not be present
    self.assertNotIn(93, avg)

  def test_get_transaction_fees(self):
    print("Running test_get_transaction_fees")
    mgr = AccountManager()

    mgr.add_account(Account(51, "Alice"))
    mgr.add_account(Account(72, "Bob"))
    mgr.add_account(Account(84, "Jane"))
    mgr.add_account(Account(97, "Frank"))
    mgr.add_account(Account(108, "Grace"))

    # Account 51: 5 transactions
    mgr.add_transaction(Transaction(1, 51, TransactionType.DEPOSIT, 100.0, 1000))
    mgr.add_transaction(Transaction(2, 51, TransactionType.WITHDRAWAL, 20.0, 1010))
    mgr.add_transaction(Transaction(3, 51, TransactionType.DEPOSIT, 10.0, 1020))
    mgr.add_transaction(Transaction(4, 51, TransactionType.WITHDRAWAL, 5.0, 1030))   # fee: $2
    mgr.add_transaction(Transaction(5, 51, TransactionType.DEPOSIT, 7.0, 1040)) # fee: $1

    # Account 72: 4 transactions
    mgr.add_transaction(Transaction(6, 72, TransactionType.WITHDRAWAL, 50.0, 2000))
    mgr.add_transaction(Transaction(7, 72, TransactionType.WITHDRAWAL, 10.0, 2010))
    mgr.add_transaction(Transaction(8, 72, TransactionType.DEPOSIT, 20.0, 2020))
    mgr.add_transaction(Transaction(9, 72, TransactionType.WITHDRAWAL, 5.0, 2030))  # fee: $2

    # Account 84: 4 transactions (added out of order, must be sorted by timestamp)
    mgr.add_transaction(Transaction(26, 84, TransactionType.WITHDRAWAL, 50.0, 2000))
    mgr.add_transaction(Transaction(27, 84, TransactionType.WITHDRAWAL, 10.0, 2010))
    mgr.add_transaction(Transaction(28, 84, TransactionType.DEPOSIT, 20.0, 2020))  # should be 4th → $1
    mgr.add_transaction(Transaction(29, 84, TransactionType.WITHDRAWAL, 5.0, 2005))

    # Account 97: 3 transactions (all free)
    mgr.add_transaction(Transaction(30, 97, TransactionType.WITHDRAWAL, 40.0, 3000))
    mgr.add_transaction(Transaction(31, 97, TransactionType.DEPOSIT, 15.0, 3010))
    mgr.add_transaction(Transaction(32, 97, TransactionType.WITHDRAWAL, 5.0, 3020))

    fees = mgr.get_transaction_fees()

    # Account 51: $2 + $1 = $3
    self.assertAlmostEqual(3.0, fees[51], places=4)

    # Account 72: $2
    self.assertAlmostEqual(2.0, fees[72], places=4)

    # Account 84: 4th transaction (chronologically) is DEPOSIT → $1
    self.assertAlmostEqual(1.0, fees[84], places=4)

    # Account 97: has only free transactions -> present with 0.0
    self.assertIn(97, fees)
    self.assertAlmostEqual(0.0, fees[97], places=4)

    # Account 108: no transactions -> omitted entirely
    self.assertNotIn(108, fees)

    # Only accounts with transactions appear: 51, 72, 84, 97
    self.assertEqual(4, len(fees))

  def test_get_suspicious_accounts(self):
    print("Running test_get_suspicious_accounts")

    mgr = AccountManager()
    mgr.add_account(Account(1, "Alice"))
    mgr.add_account(Account(2, "Bob"))
    mgr.add_account(Account(3, "Charlie"))

    # Account 1: three large withdrawals within 60 seconds -> suspicious
    mgr.add_transaction(Transaction(0, 1, TransactionType.WITHDRAWAL, 50.0,  950))
    mgr.add_transaction(Transaction(1, 1, TransactionType.WITHDRAWAL, 50.0, 1000))
    mgr.add_transaction(Transaction(2, 1, TransactionType.WITHDRAWAL, 70.0, 1030))
    mgr.add_transaction(Transaction(3, 1, TransactionType.WITHDRAWAL, 90.0, 1060))  # 1000..1060 inclusive => suspicious

    # Account 2: large withdrawals but spread out -> NOT suspicious
    mgr.add_transaction(Transaction(4, 2, TransactionType.WITHDRAWAL, 60.0, 2000))
    mgr.add_transaction(Transaction(5, 2, TransactionType.WITHDRAWAL, 80.0, 2070))
    mgr.add_transaction(Transaction(6, 2, TransactionType.WITHDRAWAL, 55.0, 2141))

    # Account 3: deposits and sub-threshold withdrawals in 60s windows -> NOT suspicious
    mgr.add_transaction(Transaction(7, 3, TransactionType.DEPOSIT, 100.0, 3010))
    mgr.add_transaction(Transaction(8, 3, TransactionType.DEPOSIT, 100.0, 3020))
    mgr.add_transaction(Transaction(9, 3, TransactionType.DEPOSIT, 100.0, 3030))
    mgr.add_transaction(Transaction(10, 3, TransactionType.WITHDRAWAL, 49.99, 3040))
    mgr.add_transaction(Transaction(11, 3, TransactionType.WITHDRAWAL, 49.99, 3050))
    mgr.add_transaction(Transaction(12, 3, TransactionType.WITHDRAWAL, 49.99, 3060))

    suspicious = mgr.get_suspicious_accounts()
    self.assertEqual([1], suspicious)

    # Account 4: three DEPOSIT transactions in 60s -> NOT suspicious
    mgr = AccountManager()
    mgr.add_account(Account(4, "Eve"))

    mgr.add_transaction(Transaction(20, 4, TransactionType.DEPOSIT, 100.0, 4000))
    mgr.add_transaction(Transaction(21, 4, TransactionType.DEPOSIT, 100.0, 4010))
    mgr.add_transaction(Transaction(22, 4, TransactionType.DEPOSIT, 100.0, 4020))

    suspicious = mgr.get_suspicious_accounts()
    self.assertEqual([], suspicious)

    # Account 10/11: large withdrawals added out of chronological order -> suspicious
    mgr = AccountManager()
    mgr.add_account(Account(11, "Donald"))
    mgr.add_account(Account(10, "Daisy"))

    mgr.add_transaction(Transaction(200, 11, TransactionType.WITHDRAWAL, 50.0, 100))
    mgr.add_transaction(Transaction(201, 11, TransactionType.WITHDRAWAL, 50.0, 120))
    mgr.add_transaction(Transaction(202, 11, TransactionType.WITHDRAWAL, 50.0, 400))
    mgr.add_transaction(Transaction(203, 11, TransactionType.WITHDRAWAL, 50.0, 140))
    mgr.add_transaction(Transaction(204, 11, TransactionType.WITHDRAWAL, 50.0, 450))

    mgr.add_transaction(Transaction(100, 10, TransactionType.WITHDRAWAL, 50.0, 500))
    mgr.add_transaction(Transaction(101, 10, TransactionType.WITHDRAWAL, 50.0, 520))
    mgr.add_transaction(Transaction(102, 10, TransactionType.WITHDRAWAL, 50.0, 800))
    mgr.add_transaction(Transaction(103, 10, TransactionType.WITHDRAWAL, 50.0, 540))
    mgr.add_transaction(Transaction(104, 10, TransactionType.WITHDRAWAL, 50.0, 950))

    suspicious = mgr.get_suspicious_accounts()
    self.assertEqual([10, 11], suspicious)


if __name__ == "__main__":
  unittest.main(exit=False)
