#!/bin/bash

cat > /app/reconcile.py <<'PYTHON'
import csv
import json
import sys
import math
from datetime import datetime, timezone


def reconcile(file_path):
    transactions = {}

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                tx_id = row["tx_id"].strip()
                timestamp = datetime.fromisoformat(
                    row["timestamp"].strip().replace("Z", "+00:00")
                )
                amount = float(row["amount"])
                status = row["status"].strip().upper()

                if not tx_id or not math.isfinite(amount):
                    continue


                if tx_id not in transactions:
                    transactions[tx_id] = {
                        "timestamp": timestamp,
                        "amount": amount,
                        "status": status
                    }
                elif timestamp > transactions[tx_id]["timestamp"]:
                    transactions[tx_id] = {
                        "timestamp": timestamp,
                        "amount": amount,
                        "status": status
                    }

            except (ValueError, KeyError, TypeError, AttributeError):
                continue

    total_valid_amount = 0.0
    valid_count = 0
    failed_count = 0

    for transaction in transactions.values():
        if transaction["status"] == "SUCCESS":
            total_valid_amount += transaction["amount"]
            valid_count += 1
        elif transaction["status"] == "FAILED":
            failed_count += 1

    return {
        "total_valid_amount": round(total_valid_amount, 2),
        "valid_count": valid_count,
        "failed_count": failed_count
    }


if len(sys.argv) != 2:
    print("Usage: python reconcile.py <csv_file>", file=sys.stderr)
    sys.exit(1)

try:
    result = reconcile(sys.argv[1])
    print(json.dumps(result))
except (OSError, csv.Error) as error:
    print(f"Error: {error}", file=sys.stderr)
    sys.exit(1)
PYTHON

echo "Reference solution applied."
