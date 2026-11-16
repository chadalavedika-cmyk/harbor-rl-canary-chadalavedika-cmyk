# Harbor RL Canary – Payment Reconciliation Bug

**Name:** Vedika Chadala  
**GitHub:** [chadalavedika-cmyk](https://github.com/chadalavedika-cmyk)  
**Task:** Payment Reconciliation Debugging  
**Model:** `groq/openai/gpt-oss-20b`  
**Tool:** Aider

## 1. About the Project

This project checks how well an AI coding agent can find and fix errors in a Python program.

The program reads payment details from a CSV file and calculates the total successful payments.

I used Harbor to run experiments and check the agent's performance.

## 2. Bugs in the Program

The original program had three main problems:

1. **Wrong calculation:** It added 1 instead of the actual payment amount.
2. **Timezone problem:** It could not correctly compare timestamps with different timezone formats.
3. **Input problem:** It used a default file when the user did not provide a CSV file path.

The program also needed better handling of duplicate and invalid records.

## 3. Experiments

I performed two experiments.

| Experiment | What I changed | Trials |
|---|---|---:|
| Baseline | Used the original instructions | 3 |
| Ablation | Added a step-by-step debugging checklist | 3 |

Both experiments used the same AI model and Aider tool.

## 4. Reward System

First, I used a simple binary reward:

- 1 if all checks passed.
- 0 if any check failed.

Later, I improved it by giving points to individual tests.

| Test | Weight |
|---|---:|
| Amount calculation | 0.20 |
| Duplicate transactions | 0.20 |
| Timezone handling | 0.20 |
| Invalid records | 0.15 |
| Command-line input | 0.10 |
| Unseen input values | 0.15 |
| **Total** | **1.00** |

The final reward is the sum of the points earned.

## 5. Testing the Solutions

I tested four different solutions.

| Solution | Reward |
|---|---:|
| No operation (nop) | 0.00 |
| Hardcoded solution (hack) | 0.00 |
| Partial solution | 0.80 |
| Complete solution (oracle) | 1.00 |

The partial solution fixed most problems but left the timezone issue. Therefore, it received 0.80.

## 6. Experiment Results

### Baseline

**Job ID:** `2026-11-16__16-24-52`

| Trial | Reward |
|---|---:|
| VgE9wx6 | 0.00 |
| 2iXAukD | 0.00 |
| SN4bEW9 | 0.00 |
| **Average** | **0.00** |

### Ablation

**Job ID:** `2026-11-16__16-30-12`

| Trial | Reward |
|---|---:|
| pa9Hdtm | 0.00 |
| KwPmnEk | 0.00 |
| aMGjTWy | 0.00 |
| **Average** | **0.00** |

The added checklist did not improve the results in these experiments.

## 7. Advantage Calculation

All six trials received a reward of zero.

| Experiment | Rewards | Average | Advantages |
|---|---|---:|---|
| Baseline | 0, 0, 0 | 0 | 0, 0, 0 |
| Ablation | 0, 0, 0 | 0 | 0, 0, 0 |

Since all rewards were the same, the advantages were zero.

The binary reward was also zero for all six trials.

## 8. Why Did the AI Fail?

I checked the available AI chat logs and test results.

The AI understood many of the problems but did not finish fixing the code.

The main problems were:

- Incorrect payment calculation.
- Incorrect duplicate transaction handling.
- Timezone comparison errors.
- Incorrect handling of invalid records.
- Missing command-line argument handling.

The agent also reached its token limit before completing the task.

## 9. Preventing Hardcoded Answers

I tested the verifier using different input values.

The hardcoded solution received 0.00, while the complete solution received 1.00.

I also tested a partial solution to confirm that the verifier gives partial marks when some bugs are fixed.

## 10. Limitations

The experiments did not generate `trajectory.json` files.

I included the available result files, Aider chat histories, logs, and test reports instead.

In future experiments, I would:
- Give the agent more time and tokens.
- Improve the debugging instructions.
- Run more trials.
- Capture complete agent action histories.
- Add more test cases.

## 11. Loom Video

https://www.loom.com/share/bb2220cbe57a416e843677d68fd69153

The Loom video demonstrates the project, including:

- Original bugs in the program.
- Partial solution and its reward (0.80).
- Complete solution and its reward (1.00).
- Hardcoded solution and its reward (0.00).
- Baseline and ablation experiment results.
- Reward and advantage calculations.
- AI agent failures and limitations.

## 12. Project Files

```text
harbor-rl-canary-chadalavedika-cmyk/
├── README.md
├── tasks/
│   └── reconcile-bug/
│       ├── task.toml
│       ├── instruction.md
│       ├── environment/
│       ├── solution/
│       └── tests/
├── jobs_summary/
│   ├── baseline/
│   └── ablation/
└── ai_transcripts/
    ├── baseline/
    └── ablation/




**Project completed by Vedika Chadala**
