import json
import subprocess
import sys
from pathlib import Path


PROGRAM = Path("/app/reconcile.py")


def run_program(tmp_path, csv_content):
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(csv_content)

    result = subprocess.run(
        [sys.executable, str(PROGRAM), str(csv_file)],
        capture_output=True,
        text=True
    )

    return result


def test_basic_transactions(tmp_path):
    csv_content = """tx_id,timestamp,amount,status
T1,2025-01-01T10:00:00+00:00,42.75,SUCCESS
T2,2025-01-01T11:00:00+00:00,50.00,FAILED
T3,2025-01-01T12:00:00+00:00,25.00,PENDING
"""
    result = run_program(tmp_path, csv_content)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["total_valid_amount"] == 42.75
    assert output["valid_count"] == 1
    assert output["failed_count"] == 1

def test_duplicate_transaction_ids(tmp_path):
    csv_content = """tx_id,timestamp,amount,status
T1,2025-01-01T10:00:00+00:00,100.00,SUCCESS
T1,2025-01-01T12:00:00+00:00,50.00,SUCCESS
"""
    result = run_program(tmp_path, csv_content)
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["total_valid_amount"] == 50.00
    assert output["valid_count"] == 1
    assert output["failed_count"] == 0

def test_timezone_comparison(tmp_path):
    csv_content = """tx_id,timestamp,amount,status
T1,2025-01-01T08:30:00+00:00,200.00,FAILED
T1,2025-01-01T09:00:00,100.00,SUCCESS
"""

    result = run_program(tmp_path, csv_content)

    assert result.returncode == 0

    output = json.loads(result.stdout)

    assert output["valid_count"] == 1
    assert output["failed_count"] == 0

def test_malformed_records(tmp_path):
    csv_content = """tx_id,timestamp,amount,status
T1,2025-01-01T10:00:00+00:00,100.00,SUCCESS
,2025-01-01T11:00:00+00:00,50.00,SUCCESS
T2,invalid-date,50.00,SUCCESS
"""

    result = run_program(tmp_path, csv_content)

    assert result.returncode == 0

    output = json.loads(result.stdout)

    assert output["total_valid_amount"] == 100.00
    assert output["valid_count"] == 1
    assert output["failed_count"] == 0

def test_missing_command_line_argument(tmp_path):
    (tmp_path / "transactions.csv").write_text(
        "tx_id,timestamp,amount,status\n"
        "T1,2025-01-01T10:00:00+00:00,100.00,SUCCESS\n"
    )

    result = subprocess.run(
        [sys.executable, str(PROGRAM)],
        cwd=tmp_path,
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert "Usage:" in result.stderr

def test_unseen_input_values(tmp_path):
    csv_content = """tx_id,timestamp,amount,status
A,2025-03-01T10:00:00+00:00,13.25,SUCCESS
B,2025-03-01T10:00:00+00:00,7.40,SUCCESS
C,2025-03-01T10:00:00+00:00,5.00,FAILED
D,2025-03-01T10:00:00+00:00,99.00,PENDING
A,2025-03-01T11:00:00+00:00,8.75,SUCCESS
"""

    result = run_program(tmp_path, csv_content)

    assert result.returncode == 0

    output = json.loads(result.stdout)

    assert output["total_valid_amount"] == 16.15
    assert output["valid_count"] == 2
    assert output["failed_count"] == 1
