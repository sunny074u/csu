# Performance Comparison Report

## What was tested

Operations were executed across increasing input sizes (n). Median runtime was used to reduce noise.

## Summary table (min/max measured time)

| ds          | op           | expected   |    min_time |   max_time |
|:------------|:-------------|:-----------|------------:|-----------:|
| Linked List | delete_value | O(n)       | 2.64e-05    |  0.0074322 |
| Linked List | insert_back  | O(1)       | 2.21999e-05 |  0.0072027 |
| Linked List | search       | O(n)       | 2.49001e-05 |  0.0076011 |
| Queue       | enqueue      | O(1)       | 1.95e-05    |  0.0054204 |
| Queue       | search       | O(n)       | 2.52e-05    |  0.0069327 |
| Stack       | push         | O(1)       | 6.19981e-06 |  0.0013827 |
| Stack       | search       | O(n)       | 6.69993e-06 |  0.0015422 |

## Prediction accuracy

| ds          | op           | expected   | inferred   | match   |
|:------------|:-------------|:-----------|:-----------|:--------|
| Stack       | push         | O(1)       | O(n)       | False   |
| Stack       | search       | O(n)       | O(n)       | True    |
| Queue       | enqueue      | O(1)       | O(n)       | False   |
| Queue       | search       | O(n)       | O(n)       | True    |
| Linked List | insert_back  | O(1)       | O(n)       | False   |
| Linked List | search       | O(n)       | O(n)       | True    |
| Linked List | delete_value | O(n)       | O(n)       | True    |

**Overall accuracy:** 57.14%


## Charts generated

- outputs/chart_stack.png
- outputs/chart_queue.png
- outputs/chart_linkedlist.png
- outputs/accuracy_overview.png
