import csv
import json
import sys
from datetime import datetime


def reconcile(file_path):
    transactions = {}

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                tx_id = row["tx_id"]
                timestamp = datetime.fromisoformat(row["timestamp"])
                amount = float(row["amount"])
                status = row["status"]

                if tx_id not in transactions:
                    transactions[tx_id] = {
                        "timestamp": timestamp,
                        "amount": amount,
                        "status": status
                    }
                else:
                    if timestamp > transactions[tx_id]["timestamp"]:
                        transactions[tx_id] = {
                            "timestamp": timestamp,
                            "amount": amount,
                            "status": status
                        }

            except (ValueError, KeyError, TypeError):
                continue

    total_valid_amount = 0
    valid_count = 0
    failed_count = 0

    for transaction in transactions.values():
        if transaction["status"] == "SUCCESS":
            total_valid_amount += 1
            valid_count += 1
        elif transaction["status"] == "FAILED":
            failed_count += 1

    result = {
        "total_valid_amount": round(total_valid_amount, 2),
        "valid_count": valid_count,
        "failed_count": failed_count
    }

    return result


if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = "transactions.csv"

result = reconcile(file_path)
print(json.dumps(result))
