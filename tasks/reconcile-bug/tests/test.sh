#!/bin/bash

reward_points=0

run_check() {
    test_path="$1"
    weight="$2"
    label="$3"

    if python -m pytest -q "$test_path"; then
        reward_points=$((reward_points + weight))
        echo "PASS: $label (+$weight points)"
    else
        echo "FAIL: $label (+0 points)"
    fi
}

mkdir -p /logs/verifier
python -m pip install -q pytest pytest-json-ctrf==0.3.5
# Check 1: Basic amount calculation (0.20)
run_check /tests/test_reconcile.py::test_basic_transactions 20 "Basic amount calculation"

# Check 2: Duplicate transaction handling (0.20)
run_check /tests/test_reconcile.py::test_duplicate_transaction_ids 20 "Duplicate transaction handling"

# Check 3: Timezone comparison (0.20)
run_check /tests/test_reconcile.py::test_timezone_comparison 20 "Timezone comparison"

# Check 4: Malformed records (0.15)
run_check /tests/test_reconcile.py::test_malformed_records 15 "Malformed records"

# Check 5: CLI argument handling (0.10)
run_check /tests/test_reconcile.py::test_missing_command_line_argument 10 "CLI argument handling"

# Check 6: Unseen input values (0.15)
run_check /tests/test_reconcile.py::test_unseen_input_values 15 "Unseen input values"

# Generate the test report
python -m pytest \
    --ctrf /logs/verifier/ctrf.json \
    /tests/test_reconcile.py -rA

# Convert points into a reward between 0.00 and 1.00
reward=$(printf "%d.%02d" "$((reward_points / 100))" "$((reward_points % 100))")

echo "$reward" > /logs/verifier/reward.txt

echo "Total score: $reward_points/100"
echo "Final reward: $reward"
