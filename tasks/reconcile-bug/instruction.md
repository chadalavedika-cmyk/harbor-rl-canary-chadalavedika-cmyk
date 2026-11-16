# Payment Reconciliation Debugging

You are given a Python command-line program called reconcile.py.
The program processes payment transaction records from a CSV file.

Your task is to debug and fix the program so that it follows the
requirements below.

## Input

The program accepts a CSV file path as a command-line argument.

The CSV contains these columns:

- tx_id: Transaction identifier(may appear in multiple rows)
- timestamp: Transaction timestamp in ISO 8601 format
  if a timestamp has no timezone offset, treat it as UTC
- amount: Transaction amount
- status: Transaction status

## Requirements

1. Read and process the supplied CSV file.
2. Handle multiple records with the same transaction ID.
3. When a transaction ID appears more than once, keep only
   the record with the latest timestamp.
4. Compare timestamps correctly, including different time zones.
5. Only transactions with status SUCCESS are valid.
6. Transactions with status FAILED must be counted as failed.
7. Transactions with status PENDING must not be included in
   either the valid or failed count.
8. Ignore malformed transaction records.
9. Calculate the total amount of valid transactions.
10. Round the total amount to two decimal places.

## Output

Print a JSON object containing exactly these fields:

- total_valid_amount
- valid_count
- failed_count

The program must execute without crashing for valid input files.

Do not hardcode expected results. Your solution must work for different CSV files.

## Recommended Debugging Workflow

Before changing the code, follow this checklist:

1. Inspect how command-line arguments are received and validate missing arguments.
2. Check how timestamps are parsed and compared, including timestamps with and without timezone information.
3. Verify that duplicate transaction IDs retain the record with the latest timestamp.
4. Check that successful transactions contribute their actual amounts to the total.
5. Verify that FAILED and PENDING transactions are counted correctly.
6. Check that malformed records are safely ignored.
7. Run the available tests after making changes.
8. Review failed tests and correct the underlying logic rather than hardcoding expected outputs.
The program must require a CSV file path as a command-line argument. If no path is provided, it must print a usage message to stderr and exit with a non-zero status.

